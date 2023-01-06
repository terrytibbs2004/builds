# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------
# Cloudflare decoder
# --------------------------------------------------------------------------------

import re
import time
import urllib
import urlparse
import requests

from decimal import Decimal, ROUND_UP


class Cloudflare:
    def __init__(self, url,check):
        response = {}
        response['code']= check.status_code
        response['url'] = url
        response['data'] = check.content
        response['error'] = None
        response['headers']= check.headers
        response['succes'] = True

        self.timeout = 8
        self.domain = urlparse.urlparse(response["url"])[1]
        self.protocol = urlparse.urlparse(response["url"])[0]
        self.js_data = {}
        self.header_data = {}

        if not "var s,t,o,p,b,r,e,a,k,i,n,g,f" in response["data"] or "chk_jschl" in response["url"]:
            return

        try:

            self.html = response['data']
            self.js_data["auth_url"] = \
                re.compile('<form id="challenge-form" action="([^"]+)" method="get">').findall(response["data"])[0]
            self.js_data["params"] = {}
            self.js_data["params"]["jschl_vc"] = \
                re.compile('<input type="hidden" name="jschl_vc" value="([^"]+)"/>').findall(response["data"])[0]
            self.js_data["params"]["pass"] = \
                re.compile('<input type="hidden" name="pass" value="([^"]+)"/>').findall(response["data"])[0]
            self.js_data["params"]["s"] = \
                re.compile(r'name="s"\svalue="(?P<s_value>[^"]+)').findall(response["data"])[0]				
            self.js_data["wait"] = int(re.compile("\}, ([\d]+)\);", re.MULTILINE).findall(response["data"])[0]) / 1000
        except Exception as e:
            print(e)
            self.js_data = {}

        if "refresh" in response["headers"]:
            try:
                self.header_data["wait"] = int(response["headers"]["refresh"].split(";")[0])
                self.header_data["auth_url"] = response["headers"]["refresh"].split("=")[1].split("?")[0]
                self.header_data["params"] = {}
                self.header_data["params"]["pass"] = response["headers"]["refresh"].split("=")[2]
            except Exception as e:
                print(e)
                self.header_data = {}

    @property
    def wait_time(self):
        if self.js_data.get("wait", 0):
            return self.js_data["wait"]
        else:
            return self.header_data.get("wait", 0)

    @property
    def is_cloudflare(self):
        return self.header_data.get("wait", 0) > 0 or self.js_data.get("wait", 0) > 0

    def get_url(self):
        # Metodo #1 (javascript)
        if self.js_data.get("wait", 0):
           # html=response['data']
            formIndex = self.html.find('id="challenge-form"')
            if formIndex == -1:
                raise Exception('Form not found')	
            subHTML = self.html[formIndex:]	
            if self.html.find('id="cf-dn-', formIndex) != -1:
                extraDIV = re.search('id="cf-dn-.*?>(.*?)<', subHTML).group(1)
                if '/' in extraDIV:
                    subsecs = extraDIV.split('/', 1)
                    extraDIV = self.parseJSString(subsecs[0]) / float(self.parseJSString(subsecs[1]))
                    print('extraDIV', extraDIV)
                else:
                    extraDIV = float(self.parseJSString(extraDIV))
            else:
                extraDIV = None
            
            # Extract the arithmetic operations.
            init = re.search('setTimeout\(function\(.*?:(.*?)}', self.html, re.DOTALL).group(1)
            builder = re.search("challenge-form'\);\s*;(.*);a.value", self.html, re.DOTALL).group(1)
            if '/' in init:
                subsecs = init.split('/')
                decryptVal = self.parseJSString(subsecs[0]) / float(self.parseJSString(subsecs[1]))
            else:
                decryptVal = self.parseJSString(init)
            lines = builder.replace(' return +(p)}();', '', 1).split(';') # Remove a function semicolon.

            for line in lines:
                if len(line) and '=' in line:
                    heading, expression = line.split('=', 1)
                    
                    if '/' in expression and not 'function' in expression:
                        subsecs = expression.split('/', 1)
                        line_val = self.parseJSString(subsecs[0]) / float(self.parseJSString(subsecs[1]))
                    
                    elif 'eval(eval(atob' in expression:
                        # Direct value function, uses the value in 'extraDIV'.
                        line_val = extraDIV
                            
                    elif '(function(p' in expression:
                        # Some expression + domain string function.                        
                        if '/' in expression:
                            subsecs = expression.split('/', 1)
                            funcSubsecsIndex = 0 if 'function' in subsecs[0] else 1
                            subsecs[funcSubsecsIndex], extraValue = self.sampleDomainFunction(subsecs[funcSubsecsIndex], self.domain)
                            line_val = self.parseJSString(subsecs[0]) / float(self.parseJSString(subsecs[1]) + extraValue)
                        else:
                            line_val = self.parseJSString(self.replaceDomainFunction(expression, self.domain))
                    else:
                        line_val = self.parseJSString(expression)

                    decryptVal = float(
                        eval(('%.16f'%decryptVal) + heading[-1] + ('%.16f'%line_val))
                    )

            answer = float('%.10f'%decryptVal)
            if '+ t.length).toFixed' in self.html:
                answer += len(self.domain) # Only old variantes add the domain length.		
		
            self.js_data["params"]["jschl_answer"] = answer

            response = "%s://%s%s?%s" % (
                self.protocol, self.domain, self.js_data["auth_url"], urllib.urlencode(self.js_data["params"]))

            time.sleep(self.js_data["wait"])

            return response

        # Metodo #2 (headers)
        if self.header_data.get("wait", 0):
            response = "%s://%s%s?%s" % (
                self.protocol, self.domain, self.header_data["auth_url"], urllib.urlencode(self.header_data["params"]))

            time.sleep(self.header_data["wait"])

            return response
			
    def sampleDomainFunction(self, section, domain):
        functionEndIndex = section.find('}')
        miniExpression = ''; parenthesisLevel = 0
        for c in section[functionEndIndex+1 : ]:
            if c == '(':
                parenthesisLevel += 1
            elif c == ')':
                parenthesisLevel -= 1
            else:
                pass
                
            if parenthesisLevel == -1:
                break
            else:
                miniExpression += c
                
        sampleIndex = self.parseJSString(miniExpression[1:-1])
        extraValue = ord(domain[sampleIndex])
        return section.split('+(function(p)', 1)[0] + ')', extraValue
        
        
    def parseJSString(self, s):
        val = int(
            eval(
                s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(', 'str(').replace('(+str', '(str').strip('+')
            )
        )
        return val
