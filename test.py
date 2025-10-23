import undetected_chromedriver as uc
print(uc.__version__)
driver = uc.Chrome()
print(driver.capabilities['browserVersion'])
driver.quit()