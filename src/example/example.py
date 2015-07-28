import argparse

__author__ = 'regu0004'


class HelloSayer(object):
    def __init__(self, lang="en"):
        self.lang = lang

    def say_hello_to(self, name):
        format_str = "{hello}, {name}"
        return format_str.format(hello=self._get_hello_phrase(),
                                 name=name)

    def say_goodbye_to(self, name):
        format_str = "{goodbye}, {name}"
        return format_str.format(goodbye=self._get_goodbye_phrase(),
                                 name=name)

    def _get_hello_phrase(self):
        if self.lang == "en":
            return "Hello"
        elif self.lang == "sv":
            return "Hej"
        else:
            return "Saluton"  # Esperanto

    def _get_goodbye_phrase(self):
        if self.lang == "en":
            return "Goodbye"
        elif self.lang == "sv":
            return "Hejdå"
        else:
            return "Adiaŭ"  # Esperanto


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("-l", dest="lang", default="en",
                        help="greeting language")
    args = parser.parse_args()

    print(HelloSayer(args.lang).say_hello_to(args.name))
