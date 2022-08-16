
class UspsScraper: 
    def __init__(self, html): 
        self.html = html


    def removeWhiteSpace(self, element): 
        return " ".join(element.strip().split())


    def findEstimatedDelivery(self):
        try: 
            eta = ""
            etaDayElement = self.html.find("em", class_="day")
            eta += etaDayElement.text

            etaDateElement = self.html.find("strong", class_="date")
            eta += " " + etaDateElement.text

            etaMonthYearElement = self.html.find("span", class_="month_year")
            eta += " " + " ".join(etaMonthYearElement.text.strip().split()[0:2])

            etaTimeElement = self.html.find("strong", class_="time")
            eta += " " + etaTimeElement.text.strip().split()[0]

            return f"Estimated Delivery by: {eta}"
        except: 
            return "No estimated delivery or the package was already delivered"


    def findTrackingHistory(self): 
        statusList = self.html.find("div", class_="panel-actions-content thPanalAction")
        spans = statusList.findAll("span")
        for span in spans:
            if span.strong: 
                timeAndDate = self.removeWhiteSpace(span.strong.text)
                print()
                print(f"Time and date: {timeAndDate}")
            elif "Shipping Partner:" in span.text:
                print(self.removeWhiteSpace(span.text))
            else: 
                print(span.text.strip())
    