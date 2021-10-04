from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as ExpCon
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Firefox()
search_key = 'spitfire'
dataset_dir = 'dataset_dir'
n_scrolls = 10

search_window_xpath = "//input[@type='text']"
accept_cookie_button_xpath = "//div[contains(text(),'Zgadzam')]"
images_xpath = "//div[1]/div[1]/span[1]/div[1]/div[1]/div[.]/a[1]/div[1]/img[1]"
more_imgs_button_xpath = "//div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/input[1]"

# program
# włączanie przeglądarki i google images, zamykanie okna z ciasteczkami
driver.get('https://google.com/imghp')
Wait(driver,30).until(ExpCon.presence_of_element_located((
    By.XPATH, accept_cookie_button_xpath)))
driver.maximize_window()
accept_cookie_button = driver.find_element_by_xpath(accept_cookie_button_xpath)
accept_cookie_button.click()
# wyszukiwanie hasła
Wait(driver,30).until(ExpCon.presence_of_element_located((
    By.XPATH, search_window_xpath)))
search_window = driver.find_element_by_xpath(search_window_xpath)
search_window.send_keys(search_key)
search_window.send_keys(Keys.RETURN)

# wyszukiwanie i pobieranie obrazów
Wait(driver,30).until(ExpCon.presence_of_element_located((
    By.XPATH, images_xpath)))
for n_scroll in range(n_scrolls):
    # skrolowanie w sam dół strony, by pojawiło się więcej obrazów
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight)")

    images = driver.find_elements_by_xpath(images_xpath)
    print(f'n_scroll:{n_scroll}, ilość obrazów: {len(images)}')
    # tak właściwie to tylko zapisy z ostatniej iteracji się liczą, poprzednie są nadpisywane. Poprzednie iteracje
    # jednak są potrzebne, by poskakać po obrazach i one się utrwaliły do tej ostatniej
    for nr, image in enumerate(images):
        with open(f'dataset_dir/{search_key}_{nr}.png', 'wb') as file:
            file.write(image.screenshot_as_png)

    # klikanie przycisku "więcej obrazów"
    if n_scroll == 5:
        driver.find_element_by_xpath(more_imgs_button_xpath).click()

# zamykanie przeglądarki
driver.close()
