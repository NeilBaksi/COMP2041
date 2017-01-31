#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI ':standard';
use CGI::Session;
use CGI::Cookie;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
warningsToBrowser(1);

use File::Basename;
use File::Path qw(mkpath rmtree);

print page_header();

sub page_header {
    
    print "<!DOCTYPE html\n",
           "PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"\n",
          "\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n",
   	      "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en-US\" xml:lang=\"en-US\">\n",
	      "<head>\n",
	        "<title>MATELOOK</title>\n",
	        "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>\n",
	         "<link rel='stylesheet' href='my_matelook.css' type='text/css'/>\n",
		# Bootstrap start --> getbootstrap.com
		"<script src='//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js'></script>\n",
		"<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css'>\n",
		"<link href='//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css' rel='stylesheet'>\n",
		# Bootstrap end
		
        print header(-charset => "utf-8"),
        start_html(-title => 'MATELOOK', -style => "my_matelook.css",),
        div({-class => "matelook_heading"}, "matelook");
        
		
}

#to find out where the link is coming from using the url
#code from http://blog.techdex.net/How_to_get_the_current_URL_in_Perl.html
$page_url .= "://";
if ($ENV{SERVER_PORT} != "80") {
	$page_url .= $ENV{SERVER_NAME}.":".$ENV{SERVER_PORT}.$ENV{REQUEST_URI};
} else {
	$page_url .= $ENV{SERVER_NAME}.$ENV{REQUEST_URI};
}
    $user_id="";
	$user_id = $page_url;
	$user_id =~ s/(\:\/\/cgi\.cse\.unsw\.edu\.au\/~z5081777\/ass2\/delete_user\.cgi\?value=)//g;
	$user_id =~ s/\%//;
	$user_id =~ s/(dataset-medium\/)//;

print "<h1 style=\"text-align:center;\">Confirm delete user $user_id\?</h1>";#/


print   "<div style=\"text-align:center;\" class=\"matelook_user_details\">\n",
            "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/matelook.cgi\">",
                "<input class=\"btn btn-info btn-lg\" type=\"submit\" name=\"confirm\" value=\"Confirm\">",
            "</form></div>";

print   "<div style=\"text-align:center;\" class=\"matelook_user_details\"'>\n",
            "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$user_id\">",
                "<input class=\"btn btn-info btn-lg\" type=\"submit\" name=\"cancel\" value=\"Cancel\">",
            "</form></div>";

if (defined param("confirm")){
    chdir "dataset-medium/";
    rmdir $user_id; 
    
}






print page_trailer();
sub page_trailer {
    print "<marquee behavior=\"alternate\">COMP2041 Assignment 2 by Supratik Baksi- z5081777</marquee>";
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}



