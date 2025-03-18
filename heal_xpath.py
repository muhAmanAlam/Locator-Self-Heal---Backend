from google import genai


def heal_xpath(xpath_name, last_working_xpath, current_dom, last_dom):
    print('Healing Xpath now')
    prompt = f'''You are a web UI test script repair tool. Your job is to repair the Xpath locator for an element that was working previously.\n'''     
    prompt += f'''The Xpath locator that was working was: {last_working_xpath}\n'''
    prompt += f'''Below is the DOM it was working on:\n'''
    prompt += f'''{last_dom}\n'''
    prompt += f'''Now, the DOM has updated and the Xpath locator is not working anymore, analyze the new DOM which is provided below and generate a new Xpath locator:\n'''
    prompt += f'''{current_dom}\n'''
    prompt += f'''Your answer should only be in one line that consists of the locator\n'''
    
    client = genai.Client(api_key="")  # Insert your Api key here
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    healed_xpath = response.text.strip()
    
    print('\nSucessfully healed Xpath')
    print('Previous: ' + last_working_xpath)
    print('Healed Xpath: ' + healed_xpath)
    
    with open("current_prompt.txt", "w") as file:
        file.write(prompt)
    
    return healed_xpath