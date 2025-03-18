from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
import logging

from db_functions import check_if_xpath_exists, fetch_xpath_entry
from heal_xpath import heal_xpath
from cleaner import clean_html


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.post("/upload_dom/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()

    # Print information about the file to the console
    logger.debug(f"File Name: {file.filename}")
    logger.debug(f"File Size: {len(content)}")
    logger.debug(f"File MIME Type: {file.content_type}")
    
    # Return information about the file to the caller - note that the
    # content_type can easily be spoofed
    
    with open("files/dom.txt", "wb") as temp:
        temp.write(content)
    
    return {"filename": file.filename, "file_size": len(content), "file_mime_type": file.content_type}



@app.get("/previous_working_xpath/{xpath_key}")
def previous_xpath(xpath_key: str):
    if check_if_xpath_exists(xpath_key):
        return {'previous_working_xpath': fetch_xpath_entry(xpath_key)[1]}
    
    else:
        raise HTTPException(status_code=404, detail="Entry for xpath does not exist in db")

    
@app.get("/heal_xpath/{xpath_key}")
def heal_xpath_locator(xpath_key: str):
    
    xpath_name, last_working_xpath, last_working_dom = fetch_xpath_entry(xpath_key)

    with open("files/dom.txt", "r") as file:
        current_dom = file.read()

    current_dom = clean_html(current_dom)
    
    with open("files/dom.txt", "w") as temp:
        temp.write(current_dom)
    
    
    healed_xpath = heal_xpath(xpath_name, last_working_xpath, current_dom, last_working_dom)
    
    with open("files/healed_xpath.txt", "w") as temp:
        temp.write(healed_xpath)
    
    return {'healed_xpath': healed_xpath}




@app.get("/save_xpath_and_dom/{xpath_key}")
def save_xpath_and_dom(xpath_key: str):
    
    with open("files/dom.txt", "r", encoding="utf-8") as file:
        current_dom = file.read()
    
    with open("files/healed_xpath.txt", "r", encoding="utf-8") as file:
        healed_xpath = file.read()
    
    update_xpath_entry(xpath_key, healed_xpath, current_dom)
    
    return {'Sucessfully Updated': xpath_key}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
