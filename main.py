# Scraper (1)
# Calculator (2)
# Review Penalizer (3)
import unittest
import pandas as pd

# I used Octoparse 8 to read data directly from the web and Power BI but it was working page by page
# as number of ratings and number of Oscar was in different poge it doesnt work efficenly I get data pof 1st page by help of Power BI
# then mantuaslly entered the values for number of ratings and number of Oscar
# then saved as excel sheet and read from it.

data = pd.read_excel(r'top_20.xlsx')
top_M20 = pd.DataFrame(data, columns=['Title', 'Rating', 'Number_Of_Ratings', 'Number_Of_Oscars'])

def scraper():
    # I understand the functions as the title check
    top_M20_col = top_M20.columns.ravel() #read titles
    return top_M20_col

def calculator():
    # 1 or 2 oscars → 0.3 point
    # 3 or 5 oscars → 0.5 point
    # 6 to 10 oscars → 1 point
    # 10+ oscars → 1.5 point
    bonus = 0
    add_rating = []
    for i in range(20):
        if top_M20['Number_Of_Oscars'].iloc[i] in range(1, 3):
            bonus = 0.3
        elif top_M20['Number_Of_Oscars'].iloc[i] in range(3, 6):
            bonus = 0.5
        elif top_M20['Number_Of_Oscars'].iloc[i] in range(6, 11):
            bonus = 1
        elif top_M20['Number_Of_Oscars'].iloc[i] > 10:
            bonus = 1.5

        added_val = round((top_M20['Rating'].iloc[i] + bonus), 1)
        add_rating.append(added_val)

    top_M20['Bonus_Oscar_Rating'] = add_rating
    # print(top_M20)
    return add_rating

def review_penalizer():
    sorted_M = data.sort_values(by=['Number_Of_Ratings'], ascending=False) #soreted data by value of Number_Of_Ratings
    max_rated = (sorted_M['Number_Of_Ratings'].iloc[0])  #max rate number
    new_rating = []
    for i in range(20):
        val = sorted_M['Number_Of_Ratings'].iloc[i]
        rating_old = top_M20['Rating'].iloc[i]
        penalized_val = round(((max_rated - val) / 100000) * 0.1, 1)  #penalty calculation
        penalized_rating = round((rating_old - penalized_val), 1)
        new_rating.append(penalized_rating)

    top_M20['Penalized_Rating'] = new_rating

    # print(top_M20)
    top_M20.to_excel('renewed_top_20.xlsx') # write the result back to excell sheet
    return new_rating

class Testing(unittest.TestCase):
    def test_func(self):
        corr_colums = ['Title', 'Rating', 'Number_Of_Ratings', 'Number_Of_Oscars']
        corr_cal_val = [9.2,9.7,9.3,10.0,10.0,9.9,10.4,9.1,9.3,9.3,9.1,9.0,9.0,9.2,9.0,9.2,9.0,9.1,9.1,9.1]
        corr_penalized_val = [9.2,9.2,8.7,8.4,8.4,8.3,8.1,8.0,8.0,8.0,7.8,7.7,7.4,7.3,7.3,7.2,7.0,6.7,6.7,6.3]

        scraper_val = scraper()
        cal_val = calculator()
        penalized_val = review_penalizer()

        self.assertEqual(scraper_val.tolist(), corr_colums)
        self.assertEqual(cal_val, corr_cal_val)
        self.assertEqual(penalized_val, corr_penalized_val)


if __name__ == '__main__':
    unittest.main()
    #print(top_M20)
    # scraper()
    # calculator()
    # review_penalizer()
