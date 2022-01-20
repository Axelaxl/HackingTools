# encoding: UTF-8
=begin

BETTERCAP

Author : Simone 'evilsocket' Margaritelli
Email  : evilsocket@gmail.com
Blog   : https://www.evilsocket.net/

This project is released under the GPL 3 license.

=end
module BetterCap
  # Current version of bettercap.
  VERSION = '1.6.1b'
  # Program banner.
  BANNER = File.read( File.dirname(__FILE__) + '/banner' ).gsub( '#VERSION#', "v#{VERSION}")
end
