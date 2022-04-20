#!/usr/bin/env python3

# Edit a jmx file as recorded by BlazeMeter to:
# - insert required listeners
# - insert referrer headers and Django CSRF tokens before POSTs
# - optionally replace selected texts with alternatives (for URLs, port numbers etcetera)

# Typical usage
# python3 jmxedit.py test1.yml --input ../crc-naive-test.jmx --output test1.jmx

import copy

from lxml import etree  # For the wonderful XPath
import yaml # For the specification
from yaml.loader import SafeLoader
from yaml.parser import ParserError

from contexts import Context

# Remove an element promoting any tail to previous sibling or parent
# per https://stackoverflow.com/questions/7981840/how-to-remove-an-element-in-lxml
def remove_element(el):
    parent = el.getparent()
    if el.tail and el.tail.strip():
        prev = el.getprevious()
        if prev:
            prev.tail = (prev.tail or '') + el.tail
        else:
            parent.text = (parent.text or '') + el.tail
    parent.remove(el)
    print ("..'%s' element removed" % el.tag)

def requireSingleNode (nodes, at, instructionPosition):
    count = len (nodes)
    if count == 0:
        raise JMXEditError ("No nodes selected by '%s' at instruction %s" %
            (at, instructionPosition)
        )
    elif count > 1:
        raise JMXEditError ("%d nodes selected by '%s' at instruction %s" %
            (count, at, instructionPosition)
        )
    return nodes [0]

def requireSingleText (nodes, at, instructionPosition):
    node = requireSingleNode (nodes, at, instructionPosition)
    if not isinstance (node, str):
        raise JMXEditError ("Path '%s' doesn't select text at instruction %s" %
            (at, instructionPosition)
        )
    return str (node)

# Check if element is a dummy wrapper, and if so replace it with its children
def undummy (el):
    if el.tag == "dummy":
        parent = el.getparent ()
        index = parent.index(el)
        parent.remove (el)
        for child in el:
            parent.insert (index, child)
            index += 1

class JMXEditError (Exception): pass

class JMXEditor:
    def __init__ (self, specification, inputJMX):
        self.specification = specification
        self.inputJMX = inputJMX
        self.context = Context ()
        self.nodeStack = []
        self.result = copy.copy (inputJMX)

    def edit (self, specification=None, thisNode=None, index=None):
        if specification is None: specification = self.specification
        if thisNode is None: thisNode = self.result
        if index is None: index = 0
        localContext = self.context.new_child ()
        instructions = specification.get ("instructions")
        if instructions is None:
            raise JMXEditError (
                "No instructions found in specification at %s" %
                self.diagnoseStack ()
            )
        elif not isinstance (instructions, list):
            raise JMXEditError ("Instructions are not a list")
        for instructionIndex, instruction in enumerate (instructions):
            self.nodeStack.append ((specification, thisNode, instructionIndex))
            #print ("Instruction", self.diagnoseStack (), instruction)
            path = instruction.get ("at")
            if path is None:
                raise JMXEditError (
                    "No path at instruction %s" % self.diagnoseStack ()
                )
            action = instruction.get ("action")
            if action is None:
                raise JMXEditError (
                    "No action at instruction %s" % self.diagnoseStack ()
                )
            try:
                nodes = thisNode.xpath (path)
            except etree.XPathEvalError as e:
                raise JMXEditError (
                    "Can't use xpath %s (%s) at instruction %s" % (
                        path, e, self.diagnoseStack ()
                    )
                )
            if nodes:
                print ("%d node(s) selected to %s for '%s' at instruction %s" %
                    (len (nodes), action, path, self.diagnoseStack ())
                )
                if action == "set":
                    text = requireSingleText (nodes, path, self.diagnoseStack ())
                    name = instruction.get ("name")
                    self.context [name] = text
                    print ("Variable '%s' set to '%s'." % (name, text))
                elif action == "remove":
                    for node in nodes:
                        remove_element (node)
                elif action == "replace":
                    for index, node in enumerate (nodes):
                        # Fresh elements for each node
                        replacement = self.getWith (instruction)
                        node.getparent ().replace (node, replacement)
                        undummy (replacement)
                elif action == "replace-text":
                    for index, node in enumerate (nodes):
                        if not isinstance (node, str):
                            raise JMXEditError ("Path '%s' doesn't select text at instruction %s" %
                                (at, instructionPosition)
                            )
                        node = instruction.get ("with")
                elif action == "wrap":
                    for index, node in enumerate (nodes):
                        wrapper = etree.fromstring (instruction.get ("with"))
                        wrappee = wrapper.xpath (instruction.get ("wrappee"))
                        node.addprevious (wrapper)
                        wrappee.getparent ().replace (wrappee, node)
                        undummy (node)
                elif action in ("first-child", "last-child", "before", "after"):
                    for index, node in enumerate (nodes):
                        newNode = etree.fromstring (instruction.get ("with"))
                        if action == "first-child":
                            node.insert (0, newNode)
                        elif action == "last-child":
                            node.append (newNode)
                        elif action == "before":
                            node.addprev (newNode)
                        elif action == "after":
                            node.addnext (newNode)
                        undummy (newNode)
                elif action == "list":
                    print ("Selected nodes: ", [(node.tag, len (node)) for node in nodes])
                else:
                    print ("Unknown action '%s' for instruction %s" %\
                        (action, self.diagnoseStack ())
                    )

            else:
                print ("No node(s) selected to %s for '%s' at instruction %s" %
                    (action, path, self.diagnoseStack ())
                )
            #    print ("Nodes", len (nodes),
            #        [node.tag for node in nodes]
            #    )
            self.nodeStack.pop ()

        return thisNode

    def diagnoseStack (self):
        return ".".join ([str (index+1) for
            _, _, index in self.nodeStack])

    def getWith (self, instruction):
        try:
            xmlDoc = etree.fromstring (instruction.get ("with"))
        except etree.XMLSyntaxError as e:
            raise JMXEditError (
                "Couldn't parse XML as with (%s) for instruction %s" %
                (e, self.diagnoseStack ())
            )
        return xmlDoc

if __name__ == "__main__":
    import argparse # For the command line
    import os
    import sys

    parser = argparse.ArgumentParser (description='Edit JMX file')
    parser.add_argument ('specificationFilename')
    parser.add_argument ('--input', dest="inputFilename")
    parser.add_argument ('--output', dest="outputFilename")

    args = parser.parse_args ()

    root, ext = os.path.splitext (args.specificationFilename)
    if not ext: args.specificationFilename += ".yaml"
    print ("..jmxedit with specification from %s" %
        args.specificationFilename
    )
    if args.inputFilename:
        root, ext = os.path.splitext (args.inputFilename)
        if not ext: args.inputFilename += ".jmx"
        print ("..Input from %s" % args.inputFilename)
    if args.outputFilename:
        root, ext = os.path.splitext (args.outputFilename)
        if not ext and not root.endswith ("null"): args.outputFilename += ".jmx"
        print ("..Output to %s" % args.outputFilename)

    # Fetch the specification
    with open(args.specificationFilename) as specificationFile:
        try:
            specification = yaml.load(specificationFile, Loader=SafeLoader)
            #print("Specification", specification)
        except ParserError as e:
            print ("--Bad yaml specification: %s" % e)
            sys.exit (0)

    with (open (args.inputFilename)
        if args.inputFilename else sys.stdin
    ) as inputFile:
        inputJMX = etree.parse (inputFile)

    editor = JMXEditor (specification, inputJMX)
    try:
        editedJMX = editor.edit ()

        with (open (args.outputFilename, "wb")
            if args.outputFilename else
            os.fdopen (sys.stdout.fileno(), "wb", closefd=False)
        ) as outputFile:
            outputFile.write (etree.tostring (editedJMX))
            outputFile.flush ()
    except JMXEditError as e:
        print ("--Edit failed: %s" % e)

