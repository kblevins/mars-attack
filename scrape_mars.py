def scrape():

    # import dependencies
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    import pandas as pd

    # chrome driver
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # get latest mars headline
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    links = soup.find_all('div', class_="list_text")

    # store headline
    headline = links[0].a.text

    # store text
    story = links[0].find('div', class_="article_teaser_body").text

    # get image from jpl
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    jpl_img = jpl_soup.find('a', class_="fancybox")

    # store full path to image
    featured_image_url = 'https://www.jpl.nasa.gov'+ jpl_img['data-fancybox-href']


    # get latest weather from twitter
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')

    weather = weather_soup.find('p', class_="tweet-text")

    # store weather info
    mars_weather = weather.text

    # get mars facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    facts_html = browser.html
    facts_soup = bs(facts_html, 'html.parser')

    # put facts into a table
    table = facts_soup.find_all('table')[0] # Grab the first table

    new_table = pd.DataFrame(columns=['description', 'fact'], index = range(0,9)) # I know the size 
        
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            new_table.iat[row_marker,column_marker] = column.get_text()
            column_marker += 1
        row_marker += 1

    # convert pandas table to html
    facts_html = new_table.to_html()

    # get hemisphere photos
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')

    hemisphere_image_urls = []

    # save to dictionary
    links = hemi_soup.find_all('div', class_="item")
    for link in links:
        h_url = 'https://astrogeology.usgs.gov' + link.find('a')['href']
        browser.visit(h_url)
        h_html = browser.html
        h_soup = bs(h_html, 'html.parser')
        hemi_link = h_soup.find('div', class_="downloads").find_all('li')[1].find('a')['href']
        hemi_title = h_soup.find('h2', class_="title").text
        hemi_title = hemi_title.replace(" Enhanced", "")
        hemi_dict = {"title": hemi_title, "url": hemi_link}
        hemisphere_image_urls.append(hemi_dict)

    # create dictionary with all scraped data
    mars = {
        "news": headline,
        "story": story,
        "image": featured_image_url,
        "weather": mars_weather,
        "facts": facts_html,
        "hemispheres": hemisphere_image_urls    
    }

    return(mars)