#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI ':standard';
use CGI::Session;
use CGI::Cookie;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
warningsToBrowser(1);



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
# basic code taken from http://www.bootply.com/
print 
"<hr><div class=\"container-fluid\">",
      "<div class=\"col-md-4 col-md-offset-4\">",
        "<div class=\"panel-body\">",
         "<div class=\"text-center\">",
            "<h2 style='color:#6A96F2' class=\"text-center\">Forgot Password?</h2>",

                  "<form class=\"form\">",
                   " <fieldset><div class=\"form-group\">",
                     "<div style=\"padding:20px;\"class=\"input-group\">",
                      "<span class=\"input-group-addon\"><i class=\"glyphicon glyphicon-envelope color-blue\"></i></span>",
                  "<input id=\"email\" placeholder=\"email address\" class=\"form-control\" name='useremail' required=\"autofocus\" type=\"email\">",
                  
                   "</div>",
                   "<p><input id=\"id\" placeholder=\"Enter z id\" class=\"form-control\" name='userid' required=\"autofocus\" type=\"id\">",
                   "</div>",
                   
                  "<div class=\"form-group\">",
                   "<input style='background-color:#6A96F2;border-color:#6A96F2;' class=\"btn btn-lg btn-primary btn-block\" value=\"Send My Password\" name='passbtn' type=\"submit\">",
               "</div></fieldset></form></div></div>",
            "</div></div>";


if (defined param("passbtn")){
    my $emailid = param("useremail");
    my $email = param("userid");
    
    my $user_filename = "dataset-medium/$email/user.txt";
        open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
        while ( my $line = <$fh> ) {         
            if ( $line =~ /(^password)/ ) {             
                $line =~ s/(^password)//;
                $line =~ s/=//;
                $line =~ s/\s*$//;
                $pass = $line;
                }    
            }         
        close $fh;
    
        `printf "Your password is : $pass \n \nLink to login page : http://cgi.cse.unsw.edu.au/~z5081777/ass2/matelook.cgi \n \nLink to your profile : http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$email\n" | /usr/sbin/sendmail $emailid`;
        
    
    print email_sent();
}

sub email_sent{
    print "<h1 style=\"text-align:center;\">Email Sent!</h1>";
     print "<div class=\"container_nxt\">",
            "<p><a href=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/matelook.cgi\" class=\"btn btn-info btn-sm\">",
                "<span class=\"glyphicon glyphicon-new-window\"></span>Go back to Login Page</a>",
            "</p>",
          "</div>";   
}











print page_trailer();
sub page_trailer {
    print "<marquee behavior=\"alternate\">COMP2041 Assignment 2 by Supratik Baksi- z5081777</marquee>";
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}
