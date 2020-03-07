def reverse(string): 
    string = string[::-1] 
    return string 

def reformat_guid(in_guid, rule):
    out_guid = ""
    if rule == "msi_component":
        out_guid = reverse(in_guid[1:9]) + \
                 reverse(in_guid[10:14]) + \
                 reverse(in_guid[15:17]) + \
                 reverse(in_guid[17:19]) + \
                 reverse(in_guid[20:22]) + \
                 reverse(in_guid[22:24]) + \
                 reverse(in_guid[25:27]) + \
                 reverse(in_guid[27:29]) + \
                 reverse(in_guid[29:31]) + \
                 reverse(in_guid[31:33]) + \
                 reverse(in_guid[33:35]) + \
                 reverse(in_guid[35:37])
    return out_guid

