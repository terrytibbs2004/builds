

import base64, codecs
magic = 'aW1wb3J0IHhibWNhZGRvbgoKdHJ5OgogICAgZnJvbSByZXNvdXJjZXMubGliLkRJIGltcG9ydCBESQogICAgZnJvbSByZXNvdXJjZXMubGliLnBsdWdpbiBpbXBvcnQgcnVuX2hvb2ssIHJlZ2lzdGVyX3JvdXRlcwpleGNlcHQgSW1wb3J0RXJyb3I6CiAgICBmcm9tIC5yZXNvdXJjZXMubGliLkRJIGltcG9ydCBESQogICAgZnJvbSAucmVzb3VyY2VzLmxpYi5wbHVnaW4gaW1wb3J0IHJ1bl9ob29rLCByZWdpc3Rlcl9yb3V0ZXMKCnRyeToKICAgIGZyb20gcmVzb3VyY2VzLmxpYi51dGlsLmNvbW1vbiBpbXBvcnQgKgpleGNlcHQgSW1wb3J0RXJyb3I6CiAgICBmcm9tIC5yZXNvdXJjZXMubGliLnV0aWwuY29tbW9uIGltcG9ydCAqCgppbXBvcnQgcmVxdWVzdHMsIG9zCmZyb20gb3MucGF0aCBpbXBvcnQgam9pbgojIGltcG9ydCB4Ym1jYWRkb24KZnJvbSB4Ym1jdmZzIGltcG9ydCB0cmFuc2xhdGVQYXRoCgphZGRvbiA9IHhibWNhZGRvbi5BZGRvbigpClVTRVJfREFUQV9ESVIgPSB0cmFuc2xhdGVQYXRoKGFkZG9uLmdldEFkZG9uSW5mbygicHJvZmlsZSIpKQpBRERPTl9EQVRBX0RJUiA9IHRyYW5zbGF0ZVBhdGgoYWRkb24uZ2V0QWRkb25JbmZvKCJwYXRoIikpClJFU09VUkNFU19ESVIgPSBvcy5wYXRoLmpvaW4oQURET05fREFUQV9ESVIsICJyZXNvdXJjZXMiLCAibGliIiwgImRhdGEiKQogCmNhY2hlX3VybCA9ICdodHRwczovL2xvb3BhZGRvbi51ay9maWxlcy9rMTkvYXJ0L2xvb3BfY2FjaGUuZGInICAgICAgICAgCmNhY2hlX2ZpbGUgPSBvcy5wYXRoLmpvaW4oUkVTT1VSQ0VTX0RJUiwgJ2xvb3BfY2FjaGUuZGInKQoKdXBkX2NhY2hlID0gJ25vJyAKdXBkX2NhY2hlID0gY2hlY2tfY2FjaGUoY2FjaGVfdXJsICwgY2FjaGVfZmlsZ'
love = 'FxXVlOxo19fo2pbMvqxMJMuqJk0VP0tL2SwnTHtqKOxLKEyVUWypJDtCFO7p3ElXUIjMS9wLJAbMFy9VPptXFNtPtccMvO1pTEsL2SwnTHhoT93MKVbXFN9CFq5MKZaVQbtPvNtVPNwVTEiK2kiMluzW2EyMzS1oUDtYFOwLJAbMFOvMJyhMlO1pTEuqTIxVPptXFNtPvNtVPOxo3qhoT9uMPuwLJAbMI91pzjfVSWSH09IHxASH19RFIVcPtccMvOipl5jLKEbYzymMzyfMFudo2yhXSWSH09IHxASH19RFIVfVPqupaEsMTS0LF5dp29hWlxcVQbto3ZhpzIgo3MyXTcinJ4bHxIGG1IFD0IGK0EWHvjtW2SlqS9xLKEuYzcmo24aXFxXPaAbo3W0K2AbMJAeMKVtCFNbJjbtVPNtW0SxMv5frFpfVNbtVPNtW0WcqP5frFpfVNbtVPNtW0AbnJkjYzy0WljtPvNtVPNaD2kwnl5lqFpfVNbtVPNtW0A1qUDhoUxaYPNXVPNtVPqRLF5aMPpfVNbtVPNtW0qcqP5colpfVNbtVPNtW2qiol5aoPpfVNbtVPNtW0ymYzqxWljtPvNtVPNaGaIfoSOinJ50MKVaYPNXVPNtVPqCpl5xLvpfVNbtVPNtW093Yzk5WljtPvNtVPNaHT8hp3DaYPNXVPNtVPqEpUZhpaHaYPNXVPNtVPqGnT9lqP5woFpfVNbtVPNtW1EcoaxhL2ZaYPNXVPNtVPqHnJ55IIWZYzAioFpfVNbtVPNtW0qcqP5colpfVNbtVPNtW1EcoaxhL2ZaYPNXVPNtVPOqXFNtPtclo290K3ugoS91pzjtCFOiq25OMTEiov5aMKEGMKE0nJ5aXPqlo290K3ugoPpcVT9lVPWznJkyBv8ioJScov54oJjvVPNtVPNXpz9iqS94oJksqKWfVQ0tVPWznJkyBv8iHRbioT9ipS9vLJAeqKOsnT9gMF5dp29hVtclo290K3ugoS91pzjtCFNanUE0pUZ6Yl9fo29jLJExo24hqJfiMzyfMKZinmR5Y2kio3NhnaAiovptPtcjoUIanJ4tCFORFF5joUIanJ4XPxOjoUIanJ4hpz91qTHbVv8vXDcxMJLtpz9iqPtcVP0+VR5iozH6PvNtVPOaMK'
god = 'RfbGlzdChyb290X3htbF91cmwpCgpAcGx1Z2luLnJvdXRlKCIvZ2V0X2xpc3QvPHBhdGg6dXJsPiIpCmRlZiBnZXRfbGlzdCh1cmw6IHN0cikgLT4gTm9uZToKICAgICNkb19sb2coZiIgUmVhZGluZyB1cmwgYXQgcm91dGUgPiAge3VybH0iICkKICAgIF9nZXRfbGlzdCh1cmwpCgpkZWYgX2dldF9saXN0KHVybCk6CiAgICAjZG9fbG9nKGYiIFJlYWRpbmcgdXJsID4gIHt1cmx9IiApCiAgICBpZiBhbnkoY2hlY2subG93ZXIoKSBpbiB1cmwubG93ZXIoKSBmb3IgY2hlY2sgaW4gc2hvcnRfY2hlY2tlcik6CiAgICAgICAgdXJsID0gREkuc2Vzc2lvbi5nZXQodXJsKS51cmwKICAgIHJlc3BvbnNlID0gcnVuX2hvb2soImdldF9saXN0IiwgdXJsKQogICAgaWYgcmVzcG9uc2U6ICAgICAgICAgICAKICAgICAgICAjZG9fbG9nKGYnZGVmYXVsdCAtIHJlc3BvbnNlID0gXG4ge3N0cihyZXNwb25zZSl9ICcgKQogICAgICAgIGlmIG93bkFkZG9uLmdldFNldHRpbmdCb29sKCJ1c2VfY2FjaGUiKSBhbmQgbm90ICJ0bWRiL3NlYXJjaCIgaW4gdXJsOgogICAgICAgICAgICBESS5kYi5zZXQodXJsLCByZXNwb25zZSkKICAgICAgICBqZW5fbGlzdCA9IHJ1bl9ob29rKCJwYXJzZV9saXN0IiwgdXJsLCByZXNwb25zZSkgCiAgICAgICAgI2RvX2xvZyhmJ2RlZmF1bHQgLSBqZW4gbGlzdCA9IFxuIHtzdHIoamVuX2xpc3QpfSAnKQogICAgICAgIGplbl9saXN0ID0gW3J1bl9ob29rKCJwcm9jZXNzX2l0ZW0iLCBpdGVtKSBmb3IgaXRlbSBpbiBqZW5fbGlzdF0KICAgICAgICBqZW5fbGlzdCA9IFsKICAgICAgICAgICAgcnVuX2hvb2soImdldF9tZXRhZGF0YSIsIGl0ZW0sIHJldHVybl9pdGVtX29uX2ZhaWx1cmU9VHJ1ZSkgZm9yIGl0ZW0gaW4gamVuX2x'
destiny = 'cp3DXVPNtVPNtVPOqVPNtVNbtVPNtVPNtVUW1oy9bo29eXPWxnKAjoTS5K2kcp3DvYPOdMJ5soTymqPxXVPNtVTIfp2H6PvNtVPNtVPNtpaIhK2uio2fbVzEcp3OfLKysoTymqPVfVSgqXDbXDUOfqJqcov5lo3I0MFtvY3OfLKysqzyxMJ8iCUOuqTt6qzyxMJ8+VvxXMTIzVUOfLKysqzyxMJ8bqzyxMJ86VUA0pvx6PvNtVPOspTkurI92nJEyolu2nJEyolxXPzEyMvOspTkurI92nJEyolu2nJEyolx6PvNtVPOcoKOipaDtLzSmMGL0PvNtVPO2nJEyo19fnJ5eVQ0tWlptPvNtVPO2nJEyolN9VTWup2H2AP51pzkmLJMyK2V2ATEyL29xMFu2nJEyolxtVPNtVPNXVPNtVTyzVPpvoTyhnlV6WlOcovOmqUVbqzyxMJ8cVQbXVPNtVPNtVPO2nJEyo19fnJ5eVQ0tpaIhK2uio2fbVaOlMI9joTS5VvjtqzyxMJ8cPvNtVPNtVPNtnJLtqzyxMJ9soTyhnlN6VNbtVPNtVPNtVPNtVPOlqJ5snT9inltvpTkurI92nJEyolVfVUMcMTIiK2kcozfcVPNtVPNtVPNXVPNtVTIfp2HtBtbtVPNtVPNtVUW1oy9bo29eXPWjoTS5K3McMTIiVvjtqzyxMJ8cPtcNpTk1M2yhYaWiqKEyXPVip2I0qTyhM3ZvXDcxMJLtp2I0qTyhM3ZbXGbXVPNtVUuvoJAuMTEiov5OMTEiovtcYz9jMJ5GMKE0nJ5apltcPtcNpTk1M2yhYaWiqKEyXPViL2kyLKWsL2SwnTHvXDcxMJLtL2kyLKWsL2SwnTHbXGbXVPNtVREWYzEvYzAfMJSlK2AuL2uyXPxXVPNtVTygpT9lqPO4Lz1wPvNtVPNwrTWgLl5moTIypPtkZQNjXDbtVPNtrTWgLl5yrTIwqKEyLaIcoUEcovtvD29hqTScozIlYyWyMaWyp2tvXDbXpzIanKA0MKWspz91qTImXUOfqJqcovxXPzEyMvOgLJyhXPx6PvNtVPOjoUIanJ4hpaIhXPxXVPNtVUWyqUIlovNjPtccMvOsK25uoJIsKlN9CFNvK19gLJyhK18vBtbtVPNtoJScovtcPt=='
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))