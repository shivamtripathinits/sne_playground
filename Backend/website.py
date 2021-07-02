class Website:
    def __init__(self,url,position,first_class,depth,date_class):
        self.url=url
        self.position=position
        self.first_class=first_class
        self.depth=depth
        self.date_class=date_class
        pass

    def print_data(self):
        print(f"Url: {self.url}\nPosition: {self.position}\nFirst Class: {self.first_class}\nDepth: {self.depth}\nDate Class: {self.date_class}")
