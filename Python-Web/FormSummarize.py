#!/usr/bin/env python
"""A small utility to print out form information.  It will summarize a
given form.

by Danny Yoo (dyoo@hkn.eecs.berkeley.edu)
"""



import htmllib
import formatter


class Form:
    def __init__(self):
        self.fields = []
        self.action = ''

    def __str__(self):
        fields = self.fields
        field_str = "\t" + '\n\t'.join(map(str, fields))
        return '---\naction: %s\nfields:\n%s' % (self.action, field_str)


class MyFormParser(htmllib.HTMLParser):
    def __init__(self):
        htmllib.HTMLParser.__init__(self, formatter.NullFormatter())
        self.forms = []
        self.currentForm = None
        self.currentSelectionName = None
        self.currentSelectionOptions = None


    def start_form(self, attributes):
        self.currentForm = Form()
        for (attr, value) in attributes:
            if attr == 'action': self.currentForm.action = value


    def end_form(self):
        self.forms.append(self.currentForm)


    def do_input(self, attributes):
        input_name, input_value, input_type = '', '', 'text'
        for (attr, value) in attributes:
            if attr == 'name': input_name = value
            elif attr == 'value': input_value = value
            elif attr == 'type': input_type = value
        self.currentForm.fields.append('name: "%s", type: "%s", value: "%s"'
                                       % (input_name, input_type, input_value))


    def start_select(self, attributes):
        for attr, value in attributes:
            if attr == 'name': self.currentSelectionName = value
        self.currentSelectionOptions = []


    def do_option(self, attributes):
        option_value = ''
        for attr, value in attributes:
            if attr == 'value': option_value = value
        self.currentSelectionOptions.append(value) ## Fixme!


    def end_select(self):
        self.currentForm.fields.append(
            'name: "%s", type: "select", choices: %s'
            % (self.currentSelectionName,
               str(self.currentSelectionOptions)))
    

    def getFormSummaries(self):
        return map(str, self.forms)


if __name__ == '__main__':
    import fileinput
    html = '\n'.join([line for line in fileinput.input()])
    parser = MyFormParser()
    parser.feed(html)
    summaries = parser.getFormSummaries()
    print '\n\n'.join(summaries)
