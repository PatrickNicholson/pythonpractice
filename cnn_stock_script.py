import urllib.request
import string
import unittest

def GetCNNStockForecast(URL,splice_starts,splice_ends):
    result = [-1,-1,-1,-1]
    html = ""
    try:
        if(len(splice_starts) != len(splice_ends)):
            return result
        html = urllib.request.urlopen(URL).read().decode("utf-8")
    except TypeError:
        return result
    except Exception:
        return result
    
    isContent = int(html.find("Content not found"))
    isForecast = int(html.find("There is no forecast data available."))
    if(isContent != -1 or isForecast != -1 or html == ""):
        return result
 
    for i in range(0, len(splice_starts)):
        istart = int(html.find(splice_starts[i])) + len(splice_starts[i])
        iend = int(html.find(splice_ends[i], istart))
        try:
            result[i] = float(html[istart:iend])
        except ValueError:
            return result

    return result



class TestGetCNNStockForecast(unittest.TestCase):
    splice_starts = ["\"BatsUS\">","median target of ","high estimate of ","low estimate of "]
    splice_ends = ["</span>",","," and",". "]
    URL = "https://money.cnn.com/quote/forecast/forecast.html?symb="
    

    def test_badinputs(self):
        self.assertEqual(GetCNNStockForecast(self.URL + "GME", self.splice_starts.pop(1),self.splice_ends),  [-1,-1,-1,-1], "Should be [-1,-1,-1,-1] when array lengths mismatch.")
        self.assertEqual(GetCNNStockForecast(self.URL + "GME", self.splice_starts.append("extra index"),self.splice_ends),  [-1,-1,-1,-1], "Should be [-1,-1,-1,-1] when array lengths mismatch.")
        self.assertEqual(GetCNNStockForecast(self.URL + "GME", ["1","2","3","4"], ["5","6","7","8"]),  [-1,-1,-1,-1], "Should be [-1,-1,-1,-1] when content cant be converted to a float.")
        self.assertEqual(GetCNNStockForecast(self.URL + "GME", 3, 'a'),  [-1,-1,-1,-1], "Should be [-1,-1,-1,-1] when splice array types are wrong.")
        self.assertEqual(GetCNNStockForecast(3, self.splice_starts,self.splice_ends),  [-1,-1,-1,-1], "Should be [-1,-1,-1,-1] when URL type is wrong.")
        self.assertEqual(GetCNNStockForecast("assddfasf", self.splice_starts,self.splice_ends),  [-1,-1,-1,-1], "Should be [-1,-1,-1,-1] when there is a bad URL.")


    def test_imaginarystocks(self):
        file1 = open("imaginarystocks.txt", "r")
        lines = file1.readlines()
        file1.close()
        for line in lines:
            ticker = str(line).strip("\n")
            result = GetCNNStockForecast(self.URL + ticker,self.splice_starts,self.splice_ends)
            for number in result:
                self.assertIs(number,-1, "Value should be -1 when getting an imaginary stock.")


    def test_availablestocks(self):
        file1 = open("availablestocks.txt", "r")
        lines = file1.readlines()
        file1.close()
        for line in lines:
            ticker = str(line).strip("\n")
            result = GetCNNStockForecast(self.URL + ticker,self.splice_starts,self.splice_ends)
            for number in result:
                self.assertIsNot(number,-1, "Value should not be -1 when getting an available stock.")
    

    def test_unavailablestocks(self):
        file1 = open("unavailablestocks.txt", "r")
        lines = file1.readlines()
        file1.close()
        for line in lines:
            ticker = str(line).strip("\n")
            result = GetCNNStockForecast(self.URL + ticker,self.splice_starts,self.splice_ends)
            for number in result:
                self.assertIs(number,-1, "Value should be -1 when getting an unavailable stock.")



if __name__ == '__main__':
    unittest.main()