"""Basic functionality"""

from utilities.utilities import check_year
from config import INSTRUCTIONS
from command_factory import CommandFactory


class App:
    """Handles the UI functionality for the application"""
    def __init__(self, book_service, io):
        self.book_service = book_service
        self.io = io
        self.commands = CommandFactory(io, book_service)
        self.running = False    

    def run(self):
        """Handles running the application"""
        self.running = True
        self.io.write("\nLUKUVINKKIKIRJASTO")

        while self.running:
            self.io.write(INSTRUCTIONS)
            vastaus = self.io.read("Komento: ")
            if not vastaus:
                self.running = False
            elif vastaus == "1":
                self._add_book()
            elif vastaus == "2":
                self._list_books()
            elif vastaus == "0":
                self.io.write("Heido!")
                self.running = False
            else:
                self.io.write("Komentoa ei löytynyt, yritä uudelleen.")

    def _add_book(self):
        self.io.write("Lisätään lukuvinkki...")
        author = self.io.read("Kirjailija: ")
        while not author:
            self.io.write("Kirjailijan nimi on lisättävä!")
            author = self.io.read("Kirjailija: ")

        title = self.io.read("Nimi: ")
        while not title:
            self.io.write("Kirjan nimi on lisättävä!")
            title = self.io.read("Nimi: ")

        check = True
        while check:
            published = self.io.read("Julkaisuvuosi: ")
            if not check_year(published):
                self.io.write("Julkaisuvuosi ei ole kelvollinen!")
            else:
                check = False

        new = self.book_service.create_book(author, title, published)
        if new == "duplicate":
            self.io.write(f"\nLukuvinkki '{author}: {title} ({published})' on jo listassa!")
        else:
            self.io.write(f"\nUusi lukuvinkki '{author}: {title} ({published})' lisätty.")

    def _list_books(self):
        self.io.write("Listataan lukuvinkit...")
        books = self.book_service.find_all_books()
        if books:
            for book in books:
                self.io.write(book)
        else:
            self.io.write("Sovellukseen ei ole tallennettu vinkkejä ):")

    def run_new(self):
        self.running = True
        while self.running:
            self.io.guide()
            command = self.io.read("Komento: ")
            self.commands.get_command(command).perform()
