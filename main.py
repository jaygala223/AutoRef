# URL of the form
url = "https://www.myworkday.com/intel/d/task/2997$6500.htmld"

import requests

response = requests.get(url)

text = response.text

import re

while "redirectUrl" in text or "SAMLRequest" in text or "urlLogin" in text:
    print("redirecting ...")
    
    url_pattern = r"https://[^\s\"']+"

    # Find the URL in the string
    match = re.search(url_pattern, response.text)

    # Extract the URL if found
    if match:
        new_url = match.group(0)
        print(new_url)

    if "urlLogin" in text:
        login_url_pattern = r'"urlLogin":"(https://[^"]+)"'
        match = re.search(login_url_pattern, text)

        # Extract the value if found
        if match:
            login_url = match.group(1)
            print(login_url)
            
        # response = requests.get(login_url)
        break
    
    elif "SAMLRequest" in text:
        # Regular expression to match only the value of the `value` attribute
        value_pattern = r'value="([^"]+)"'

        match = re.search(value_pattern, text)

        # Extract the value if found
        if match:
            saml_request_value = match.group(1)
            files = {'SAMLRequest': saml_request_value}
        response = requests.post(new_url, data=files)
    else:
        response = requests.get(new_url)
    text = response.text

# url = 'https://login.microsoftonline.com/46c98d88-e344-4ed4-8496-4ed7712e255d/reprocess?ctx=rQQIARAA42KwkskoKSmw0tcvLy_XK88vyk5JrNRLzs_Vz8wrSc0pEuISOCNrZC3S8suhKazpQIixKcMqRgOQlmKontxKDF36OfnpmXm6xYm5OXoZJbk5KYcYVeONLJOMk1JSLXVTDBLNdU0MUix1Lc1TEnWNTSzMki3S0pJSjVMuMDK-YGS8xcQaDNRqtIlZxcQs2dIixcJCN9XYxETXJDXFRNfCxNIMxDI3NzRKNTI1TbnAwvODhXERK9Cpv7zYud4xH3PdtGfaApEb8QynWPUjfdONCjMC9U1ctA2d86vKki0LK1OCzLMjUwq9XYqNsyKTHMtKPUOy00ItbM2tDCew8Z5iY_jAxtjBzjCLneEAJ-MBXoYffHdf3_61b_rGdx6v-HUMHCv98qpC0jwc9SvcLYtMKrWT8zICisxT9LP8TQr9DCvcTILLnZyKXMw8bTcIMDwQYAAA0'

# r = requests.get(url, timeout=5)
# print(r.text)
