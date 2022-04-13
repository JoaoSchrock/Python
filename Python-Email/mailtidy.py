#!/usr/bin/env python

"""Remove duplicate email from unix mailboxes.

mailtidy.py

John J. Lee, 2001-08-16

The contents of this file are placed in the public domain.


Remember to back up your mail before running it through this script!

Please note that this is code has only been tested by me.  If it 'tidies' your
mail into oblivion, blame yourself, not me.  As far as I know, it works, but do
back up your mail before using this.

Type mailtidy.py for usage.

Unix mailboxes are the kind where a 'folder' is represented as a file
containing plain text (RFC 822) messages, each beginning with a blank line,
followed by a line starting with 'From ' (note the space and lack of a ':').
There seems to be some variation in the exact format of this 'From ' line: if
your mailboxes aren't recognized, try modifying the regular expression below.
"""

import os, sys, mailbox, time

class MyUnixMailbox(mailbox.UnixMailbox):
    # standard Python lib regexp is not sufficiently general for my mailboxes
    _fromlinepattern = r"From \s*[^\s]+\s+\w\w\w\s+\w\w\w\s+\d?\d\s+" \
                       r"\d?\d:\d\d(:\d\d)?(\s+[^\s]+)?\s+\+?\d\d\d\d\s*$"


class UnixMailboxWriter:
    def __init__(self, fh):
        self.fh = fh

    def write(self, msg):
        """Write an rfc822.Message to file."""
        date = time.ctime(time.time())
        from_line = "From mailtidy@localhost %s\n" % (date,)
        self.fh.write(from_line)
        for l in msg.headers:
            self.fh.write(l)
        self.fh.write("\n")
        ls = msg.fp.readlines()
        for l in ls:
            self.fh.write(l)


class MailTidier:
    # messages are considered identical iff these headers are identical
    id_header_names = "Message-ID", "Date"
    def __init__(self, extension=".tidied", clobber=0):
        """
        Cleaned mailboxes are saved under the original filename with the
        extension appended, unless clobber is true, in which case the original
        mailboxes are overwritten by the tidied ones after the mailbox has been
        scanned.
        """
        self.clobber = clobber
        self.extension = extension
        self.mailboxes = []
        self.copies = {}

    def add(self, mailbox, filename):
        """Add a mailbox.

        XXX not all mailbox types are organised per-file.
        """
        self.mailboxes.append((mailbox, filename))

    def tidy(self):
        """Remove duplicate messages from all mailboxes."""
        for mb, filename in self.mailboxes:
            print "scanning", filename
            fh_out = open(filename+self.extension, "w")
            mb_out = UnixMailboxWriter(fh_out)
            msg = mb.next()
            if msg is None:
                print "empty mailbox, ignoring"
                continue
            while msg is not None:
                id = tuple([msg.get(hn) for hn in self.id_header_names])
                if not self.copies.has_key(id):  # message not yet written
                    self.copies[id] = 1
                    mb_out.write(msg)
                else:
                    self.copies[id] += 1
                copies = self.copies[id]
                if copies != 1:
                    print "duplicate #%d found" % (copies-1)
                msg = mb.next()
            fh_out.close()
            if self.clobber:
                os.remove(filename)
                os.rename(filename+self.extension, filename)


def files_in_dir(dir, ext):
    # non-recursive
    files = os.listdir(dir)
    return [os.path.join(dir, file) for file in files if (
        not os.path.isfile(file) and
        not file.endswith(ext))]

def tidy(files):
    """Remove all duplicate emails from list of directories and files.

    Non-recursive for directories.
    """
    ext = ".tidied"
    mt = MailTidier(ext, clobber=1)
    all_files = []
    for file in files:
        if os.path.isdir(file):
            all_files.extend(files_in_dir(file, ext))
        else:
            all_files.append(file)
    for file in all_files:
        mb = MyUnixMailbox(open(file))
        mt.add(mb, file)
    mt.tidy()

def main():
    if len(sys.argv) <= 1:
        print ("usage: mailtidy.py (FILE | DIRECTORY) ...\n"
               "\n"
               "Duplicate messages are removed from the unix mailbox files "
               "specified.\n"
               "\n"
               "Mailbox files are specified by listing their filenames and the "
               "names of \n"
               "directories containing mailbox files (subdirectories are not "
               "scanned).\n"
               "\n"
               "Duplicate messages are removed across files, not just within "
               "them.\n")
    filenames = sys.argv[1:]
    tidy(filenames)


if __name__ == "__main__":
    main()