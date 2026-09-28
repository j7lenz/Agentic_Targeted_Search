

#STEP 1: PLANNING

"""

1) Create a simple visual or step by step plan for how to achieve what we want:

    a) Identify which websites or repositories hold the information we are looking for
    b) Identify which tools, libraries, or resources would be relevant to scraping or fetching this information
    c) Develop step - step plan  for research-
        -> Route #1- Shortlist of VC funds that we are know are affiliated with CIC community/ecosystem - Use these to work backwards to identify the portfolio companies affiliated
        -> Route #2- We work solely from the BuiltInBoston companies list
        -> Route #3- Shortlist from the Kendall Square Association and MassBio Association - Search and scrape agents
        -> Route #4- Find the intersection of each of these- this should give us probably the closest approximation to a list of curated companies living inside the CIC walls

    d) Develop step - step plan for aggregation, searching, and cross-referencing

    e) Identify what guardrails are most important here- WHAT CAN GO WRONG HERE?-
    -> Returning matches that are not located in the correct area
    -> Returning mathches that don't fit the company size parameters
    -> Returning fake or fraudulent companies that don't exist
    -> Returning acquired, closed, or otherwise insolvent entities
    -> Search returning the wrong company description/details due to mix up
    -> Agent fails to return details in the desired schema format

    f) Web Scrape from BuiltinBoston Company directory to identify what companies are valid within the Boston area

    g) Cross-reference details and close the loop -> generate the company names 

    h) Develop step-step data enrichment plan- Enrich with details on industry, company size, description, etc...


2) Identify upfront any dependency/version conflicts that could occur due to library imports-
    a) Importing Langchain, LangGraph, and CrewAI - These versions will be highly likely to conflict with packages like pytorch, transformers, etc..
    b) Identify virtual environment requirements


3) Simple Proof of Concept using just Web Scraping and Selenium first
    A) Using XPATH to locate and identify the key buttons to click in- Much more versatile and resilient than using raw HTML 
    B) Automate clicking buttons and navigating the UI interface
    C) Able to correctly filter through the companies successfully without issues! - This is a partial step in the right direction (1/2 of what we want, now we have to scrape the entries)
    D) Identify where the data truly lives in terms of website layout:
        -> Descriptions- live inside <strong> and <p> tags
        -> Office locations- live inside span and aria label tags
        -> Href/website links- live underneath the company row's div table
    
    E) Different entity details are hidden in different places- this needs to be accounted for effectively!
    F) Work out effective end to end path to take
    -> How to scrape different things- using different tags, etc..
    -> What we can vs. cannot easily get from scraping, limitations, etc..
    -> Handling pagination- how do we ensure the application can gracefully handle page changes

    G) Outcomes from POC- learnings and remaining weak spots
    -> The core workflows remains the same, the only thing that changes is how you scrape the website. This requires strong judgement and thinking around what breaks later.
    -> This successfully handled scraping 32 pages from the hybrid companies list, but failed to scrape the final page of results. This needs to be fixed in next iteration.
    -> Error and Exception handling are critical with web scraping - the existing checks are functional but not production ready. This needs to be fixed in next iteration.
    -> Speed - While this successfully scraped ~650 records it took nearly 2 hours to complete. Performance appears to be a challenge here. However, in real life you wouldn't scrape each entry sequentially you'd store the details.


4) Evolving from Proof of Concept Design to Production Readiness:
    A)  Scope out the key entities involved in the system-
        -> BasesiteSearch and Navigation - making the site useful for scraping bots
        -> Handling hierarchial data - company level data - need to determine the most appropriate way to model this for persistent or cloud storage
        -> Scraping - Execution
        -> Storage
    
    B) Redesign the workflow as simply as possible
    ##### SIMPLEST RE-DESIGN EFFORTS - SUBDIVIDE THE PARTS OF THE WORKFLOW

    Part I- Base - initialization of the driver, passing the url -> Highly standardized, required for all future steps- Should be enforced somehow
    Part II- Search Landscape- Browse the search and filter contents so we only scrape what we need -> Highly standardized, and this probably should be enforced as well
    Part III- Scrape Subset - This is where the real architectural decisions show up. When do we scrape (what frequency), what fields do we scrape (relevancy), and how do we validate
    the data hasn't changed (consistency). Can this handle batch only or can this support real-time? What are the boundaries between Search, Scrape, and Storage layers
    Part IV- The Storage Layer - This is where the next layer of decisions come in- where to store efficiently, how to keep data consistent across multiple scrapes, handling duplicate scrapes, etc..
    Part V- The Orchestrator - This is the brains of the scraper that control the schedule for scraping, the real-time fetches if the data being requested doesn't exist, and has the guardrails needed to ensure scraping doesn't blow up








    


    

    




















"""




#Import Required Packages
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from typing import Protocol
from dataclasses import dataclass



class BaseSiteSearch(Protocol):
    """
    -Filtering for office type
    -Filtering for industry
    -Filtering for Company Size
    """

    def filter_by_office_type():
        ...

    def filter_by_industry_sectors():
        ...

    def filter_by_company_size():
        ...





class CompanySearch(Protocol):
    """
    Gathering company details
    """
    
    @property
    def __fetch_internals():
        """
        Fetches the company profile id
        """
        pass

    def fetch_basic_level():
            #One card to navigate- MUST BE CLEARLY AND EXPLICITLY DESCRIBED/IMPLEMENTED!
            #Fetching basic level details like website link and company name
            pass

    def fetch_intermediate_level():
        #This probes futher into office locations
        pass

    def fetch_comprehensive_level():
        #this probes company details, descriptions, etc..
        pass

    def fetch_advanced_level():
        #This probes internal details like work-life balance, etc...
        pass



class Orchestrate_Web_Scrape():
    pass



    





















"""
**Desired Content to Scrape
"<div id="g_id_onload" data-client_id="941473408521-r82mlse6rh2ar9loff8bgnbqtbp6inrs.apps.googleusercontent.com" data-login_uri="https://accounts.builtin.com/External/OneTap" data-new_user_return_url="https://www.builtinboston.com/auth/login?destination=%2Fcompanies" data-existing_user_return_url="https://www.builtinboston.com/auth/login?destination=%2Fcompanies" data-auto_select="true" data-prompt_parent_id="g_id_onload" style="position: absolute; top: 150px; right: 410px; width: 0; height: 0; z-index: 1001"><div><script src="https://accounts.google.com/gsi/client" async="" defer=""></script></div></div>"

"""







#Basic Implementation Below
driver = webdriver.Chrome()
#Create empty list to store our scraped output
scraped_data = []

try:
    driver.get("https://www.builtinboston.com/companies")
    driver.implicitly_wait(10) #Wait up to 10 seconds before crashing
    #elem = driver.find_element(By.ID, "header-container")
    #print(elem.text)
    elem2 = driver.find_element(By.XPATH, "//*[@id='header-container']/div[3]/div/div[1]/div/button")  #Locate Office Type Dropdown
    elem2.click()

    #Sleep for 2-3 seconds to ensure the page loads
    time.sleep(2)

    #Search for desired companies

    hybrid_companies = driver.find_element(By.ID, "office-type-hybrid")

    if not hybrid_companies:
        raise ValueError("Unable to locate desired element")

    hybrid_companies.click()

    #Once in good shape click apply button to get the rest of the results

    #Finally click Apply to get the rest of the results
    apply_filters_button = driver.find_element(By.CSS_SELECTOR, "#office-type-dropdown-menu > div.d-flex.justify-content-between.bottom-0.border-top.p-sm > button.btn.btn-primary.btn-lg.font-montserrat-button.text-uppercase.text-white")

    if not apply_filters_button:
        raise ValueError(
            "Unable to find the desired element"
        )

    else:
        print("Successfully located the apply filters button")

    apply_filters_button.click() #Click the button to apply the filters

    #Sleep 2-3 seconds to give the page time to reload
    time.sleep(3)

    #Reload the page to the filtered list of companies - NOW WE NEED TO SCRAPE THESE!
    #Find the main container
    main_company_container = driver.find_element(By.ID, "main-container")

    if not main_company_container:
        raise ValueError(
            "Unable to locate desired element"
        )

    else:
        print("Successfully located element")
        #Pull the href out of it

    container = driver.find_element(By.XPATH, "//div[contains(@x-data, 'CompanyCardHorizontal')]")

    if not container:
        raise ValueError(
            "Unable to locate desired element"
        )

    else:
        print("Found identified elements")

    #Find the company links
    #company_links = driver.find_elements(By.XPATH, "//div[@x-data]//a[@href]")
    company_boxes = driver.find_elements(By.CSS_SELECTOR, "div.CompanyCardHorizontal") 

    total_links = len(company_boxes)
    print(f"📊 Validation Check: Found {total_links} total href links underneath the container.")

    current_page = 1

    while True:
        print(f"\n📄 --- STARTING EXTRACTION FOR PAGE {current_page} ---")

        company_cards = driver.find_elements(By.CSS_SELECTOR, ".company-card-grid")
        print(f"Option A (.company-card-grid) count: {len(company_cards)}") #Either one of these will likely work without issues!!!

        # Test 2: Check if 'company-content-area' is the repeating card
        content_areas = driver.find_elements(By.CSS_SELECTOR, ".company-content-area")
        print(f"Option B (.company-content-area) count: {len(content_areas)}")

        for index, row in enumerate(company_cards, 1):
            #Extract the metadata for each company out
            time.sleep(1)

            #### SEARCHING TOP LEVEL DETAILS FOR EACH COMPANY ###
            try:
                link_element = row.find_element(By.CSS_SELECTOR, '.company-info-section a')
                company_name = link_element.text
                website_url = link_element.get_attribute('href')
                company_profile_id = link_element.get_attribute('data-company-id')
                time.sleep(1)
            
            except Exception as e:
                print(f" Unable to locate a valid website or url link: {link_element.text}")


            ### IDENTIFYING OFFICE LOCATIONS ###
            try:
                #locate office records
                office_element = row.find_element(By.XPATH, ".//span[@aria-label='Office locations']")
                #Extract and clean records
                offices = office_element.get_attribute('data-bs-title')
                city_list = offices.replace("<br/>", ", ")
                time.sleep(1)

            except Exception as e:
                print(f" Unable to locate a valid office address: {offices}")


            ### IDENTIFYING COMPANY DETAILS AND DESCRIPTIONS ###
            try:
                description_element = row.find_element(By.CSS_SELECTOR, ".company-tagline-4-rows p")
                company_description = description_element.text

                employee_element = row.find_element(By.XPATH, ".//i[contains(@class, 'fa-user-group')]/following-sibling::span")
                employee_count = employee_element.text.replace('Employees', '')

                #industry_element=row.find_element(By.CSS_SELECTOR, ".font-barlow fw-medium text-gray-04 mb-xl-sm d-none d-lg-block")
                #industry_segments= industry_element.text

                time.sleep(1)

                ### Store elements
                 ### AGGREGATE ALL THE SCRAPED DATA RESULTS FOR EACH ENTITY ###
                            #Store internally in structured dictionary
                company_record = {
                        'name': company_name,
                        'website_link': website_url,
                        'offices': city_list,
                        #'sectors': industry_segments
                        'profile_id': company_profile_id,
                        'num_employees': employee_count,
                        'company_description': company_description
                        
                }
                

                print(f"Successully scraped data for company name: {company_name}")

                scraped_data.append(company_record)
                

            except Exception as e:
                pass

                #print(f" Unable to locate description element: {company_description}")


            ##IDENTIFYING OTHER DETAILS ###

        """ CHECKING NEXT PAGE DETAILS """
        next_page_number = current_page + 1

        
        #Target the next page for scraping
        selector_string = f"#pagination-container li:has(a[aria-label*='Page {next_page_number}'])"
        next_page_candidates = driver.find_elements(By.CSS_SELECTOR, selector_string)

        if len(next_page_candidates) > 0:
            next_button = next_page_candidates[0]
            clickable_link = next_button.find_element(By.CSS_SELECTOR, "a")
            print(f"➡️ Found the link for Page {next_page_number}. Clicking forward...")

            try:
                clickable_link.click()
            except Exception as click_err:
                print("⚠️ Standard click intercepted. Forcing click via JavaScript...")
                # FORCE the click bypassing all visual overlays
                driver.execute_script("arguments[0].click();", clickable_link)


            time.sleep(20) #Give the page time to fully load

            #Increment the page num counter
            current_page = next_page_number

        else:
            # If aria-label="Go to Page X" cannot be found, it means page X doesn't exist!
            print(f"🏁 Could not find a link for Page {next_page_number}. You have reached the end of the list!")
            break

        

#except Exception as e:
#        print(f"⚠️ Company {index}: Could not find the link inside this block. Error: {e}")

except Exception as e:
        # If one row fails (e.g., a missing location tag), the loop keeps running
        print(f"⚠️ Skipped an item due to missing details: {e}")

finally:
    driver.close()
    driver.quit()


print("Completed Web Scraping Data and Details:/n")
print("\n🎉 Final Scraped Dataset:")


#Key Columns Scraped: Company Name, Profile ID, Offices, Company Description, Website Link, Number of Employees, OTHER DETAILS, ETC.... 
### INDUSTRY / SECTOR NAME OR DETAILS
### NUMBER OF EMPLOYEES OR EMPLOYEE CATEGORY


final_df = pd.DataFrame(scraped_data)

print(final_df)

print("Columns in Dataframe:\n")
print(final_df.columns)


### EXPORT TO CSV FILE SAFELY ###
final_df.to_csv('BuiltinBoston_Export_HybridCo.csv', index=False)












