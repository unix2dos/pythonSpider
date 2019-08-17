from selenium import webdriver
from selenium.webdriver.common.keys import Keys



browser = webdriver.Chrome(executable_path="./drivers/chromedriver")
browser.get('http://www.baidu.com/')



# kw = browser.find_element_by_id("kw")
# kw.send_keys("Selenium", Keys.RETURN)


# kw = browser.find_element_by_id("kw")
# su = browser.find_element_by_id("su")
# kw.send_keys("Selenium")
# su.click()



# kw = browser.find_element_by_id("kw")
# kw.send_keys("Selenium")
# kw.submit()




browser.execute_script(
    '''
    var kw = document.getElementById('kw');
    var su = document.getElementById('su');
    kw.value = 'Selenium';
    su.click();
    '''
)
