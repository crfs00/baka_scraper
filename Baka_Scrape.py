from requests_html import HTML, HTMLSession


class Baka_Scraper:
    manga_name_str = ''
    description_str = ''
    genre_list = ''
    genre_slice_end = ''
    genre_ctrl_list = ['Shounen', 'Shoujo', 'Seinen', 'Josei']
    demographic_str = ''
    category_list = ''
    author = ''
    artist = ''
    manga_year = ''
    baka_html = ''

    def pull_baka_page(site):
        session = HTMLSession()
        r = session.get(site)

        with open('page2scrape.html', 'w', encoding='UTF-8') as f:
            f.write(r.text)

    def scrape_baka_page():
        with open('page2scrape.html', encoding='UTF-8') as f:
            Baka_Scraper.baka_html = HTML(html=f.read())

        Baka_Scraper._name_description_year()
        Baka_Scraper._author_artist()
        Baka_Scraper._genre_demographic()
        Baka_Scraper._category()

    def _name_description_year():

        Baka_Scraper.manga_name_str = Baka_Scraper.baka_html.find('.releasestitle')[0].text

        try:
            Baka_Scraper.description = Baka_Scraper.baka_html.find('#div_desc_more')[0].text.replace('Less...', '')
        except Exception as e:
            Baka_Scraper.description = Baka_Scraper.baka_html.find('div.sContent')[0].text

        Baka_Scraper.manga_year = Baka_Scraper.baka_html.find('div.sContent')[20].text

    def _author_artist():
        Baka_Scraper.author = Baka_Scraper.baka_html.find('div.sContent')[18].text
        if Baka_Scraper.author.endswith(']'):
            Baka_Scraper.author = Baka_Scraper.author[:-8]

        Baka_Scraper.artist = Baka_Scraper.baka_html.find('div.sContent')[19].text
        if Baka_Scraper.artist.endswith(']'):
            Baka_Scraper.artist = Baka_Scraper.artist[:-8]

    def _genre_demographic():
        Baka_Scraper.genre_list = Baka_Scraper.baka_html.find('div.sContent')[14].text.split('\n')
        Baka_Scraper.genre_slice_end = Baka_Scraper.genre_list.index('')
        Baka_Scraper.genre_list = Baka_Scraper.genre_list[:Baka_Scraper.genre_slice_end]

        for x in range(len(Baka_Scraper.genre_ctrl_list)):
            if Baka_Scraper.genre_ctrl_list[x] in Baka_Scraper.genre_list:

                Baka_Scraper.demographic_str = Baka_Scraper.genre_list.pop(Baka_Scraper.genre_list.index(Baka_Scraper.genre_ctrl_list[x]))

                break

    def _category():
        '''
        Meant to pull all of the categories but a link must be clicked in order to access all of them.
        For now this function will only pull the first ten catagories.
        '''
        Baka_Scraper.category_list = Baka_Scraper.baka_html.find('ul')[1].text.split('\n')

    def show():
        '''Display the scraped information in an easy to read format'''
        print(f'Name: {Baka_Scraper.manga_name_str}\n\nDescription: {Baka_Scraper.description}\n\nGenres: {Baka_Scraper.genre_list}\n\nDemographic: {Baka_Scraper.demographic_str}\n\nTags: {Baka_Scraper.category_list}\n\nAuthor: {Baka_Scraper.author}\n\nArtist: {Baka_Scraper.artist}\n\nYear Published: {Baka_Scraper.manga_year}')

    def _write():
        '''This method will write the print statement of  Baka_Scraper.show() to a text file'''
        pass


if __name__ == '__main__':

    # Baka_Scraper.pull_baka_page('https://www.mangaupdates.com/series.html?id=151340')
    Baka_Scraper.scrape_baka_page()
    Baka_Scraper.show()
