<p align="center"><img src="https://github.com/deltaxflux/fluxion/blob/master/logos/logo1.jpg?raw=true" /></p>
#Fluxion is the future of MITM WPA attacks
Fluxion is a remake of linset by vk496 with (hopefully) less bugs and more functionality. It's compatible with the latest release of Kali (rolling). Latest builds (stable) and (beta) can be found here [here] (https://sourceforge.net/projects/wififluxion/files/?source=navbar). If you're new, or just don't understand much about the project, have a look at the [wiki] (https://github.com/deltaxflux/fluxion/wiki/Tutorial). The attack is mostly manual, but experimental versions will automatically handle most functionality from the stable releases.

### "Clients are not automatically connected to the fake access point"
This is a social engineering attack and it's pointless to drag clients in automatically. The script relies on the fact that a user should be present in order to enter the wireless credentials.

### "There's no Internet connectivity in the fake access point"
There shouldn't be one. All of the traffic is being sinkholed to the built in captive portal via a fake DNS responder in order to capture the credentials.

#### "Fake sites don't work"
There might be a problem with lighttpd. The experimental version is tested on lighttpd 1.439-1, anything neweer may break functionality. If you have problems, please use the stable version. For more information check this [fix] (https://github.com/deltaxflux/fluxion/wiki/fix) out.

#### "Experimental menu is not responsive"
In the experimental version it will automatically check the handshake. I will fix the menu shortly. If you need a GUI, use the stable version (which doesn't automatically control handshakes).

#### "I need to sign in (on Android)"
This is how the script works. The fake captive portal is set up by the script itself to collect the credentials. Don't freak, it's al okay.

#### "The MAC address of the fake access point differs from the original"
The MAC address of the fake access point differs by one octet from the original in order to prevent fluxion deauthenticating clients from itself during the session. 

## Updates
If you want to submit a feature, do so by labeling your issue as an "enhancement" or submit a PR. I don't have enough time to make daily changes to fluxion, sorry.

## Included dependency versions
1. Aircrack : 1:1.2-0~rc4-0parrot0
2. Lighttpd : 1.439-1
3. Hostapd  : 1:2.3-2.3 _If you want to compare this type `dpkg -l | grep "name"`_

## :scroll: Changelog
Fluxion gets weekly updates with new features, improvements and bugfixes.
Be sure to check out the [changelog here] (https://github.com/deltaxflux/fluxion).

## :octocat: How to contribute
All contributions are welcome! Code, documentation, graphics or even design suggestions are welcome; use GitHub to its fullest. Submit pull requests, contribute tutorials or other wiki content -- whatever you have to offer, it would be appreciated!

## Support us!
Fluxion wasn't created for monetary gains. If you want to support us in a financial way, you're more than welcome to do so through the provided Bitcoin address: 1EL4asZh5bsdtt7ECwLQmypeyC2e1TqvmW

## :book: How it works
* Scan the networks.
* Capture a handshake (can't be used without a valid handshake, it's necessary to verify the password)
* Use WEB Interface *
* Launch a FakeAP instance to imitate the original access point
* Spawns a MDK3 process, which deauthenticates all users connected to the target network, so they can be lured to connect to the FakeAP and enter the WPA password.
* A fake DNS server is launched in order to capture all DNS requests and redirect them to the host running the script
* A captive portal is launched in order to serve a page, which prompts the user to enter their WPA password
* Each submitted password is verified by the handshake captured earlier
* The attack will automatically terminate, as soon as a correct password is submitted

## :heavy_exclamation_mark: Requirements

A Linux-based operating system. We recommend Kali Linux 2 or Kali 2016.1 rolling. Kali 2 & 2016 support the latest aircrack-ng versions. An external wifi card is recommended.

## :octocat: Credits
1. l3op - contributor
2. dlinkproto - contributor
3. vk496 - developer of linset
4. Derv82 - @Wifite/2
5. Princeofguilty - @webpages
6. Photos for wiki @http://www.kalitutorials.net
7. Ons Ali @wallpaper

## Useful links
 1. [Wifislax] (http://www.wifislax.com/)
 2. [Kali Linux] (https://www.kali.org/)
 3. [linset] (https://github.com/vk496/linset)
 4. [ares] (https://github.com/deltaxflux/ares)
 5. [Closeme] (https://github.com/rad4day/GithubScripts)

## Disclaimer

***Fluxion is intended to be used for legal security purposes only, and you should only use it to protect networks/hosts you own or have permission to test. Any other use is not the responsibility of the developer(s).  Be sure that you understand and are complying with the Fluxion licenses and laws in your area.  In other words, don't be stupid, don't be an asshole, and use this tool responsibly and legally.***
