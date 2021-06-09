from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

l=[]
class MyHTMLParser(HTMLParser):
   flag = 0
   def handle_starttag(self, tag, attrs):
      #print "Start tag:", tag
      if tag == 'td':
         l.append(tag)
      #for attr in attrs:
      #print "     attr:", attr

   def handle_endtag(self, tag):
      #print "End tag  :", tag
      if tag == 'td':
         l.append(tag)

   def handle_data(self, data):
      #print "Data     :", data
      l.append(data)

   def handle_comment(self, data):
      pass
      #print "Comment  :", data

   def handle_entityref(self, name):
      c = unichr(name2codepoint[name])
      #print "Named ent:", c

   def handle_charref(self, name):
      if name.startswith('x'):
         c = unichr(int(name[1:], 16))
      else:
         c = unichr(int(name))
      #print "Num ent  :", c

   def handle_decl(self, data):
      pass
      #print "Decl     :", data
