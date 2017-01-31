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




my $users_dir = "dataset-medium";
my @users = sort(glob("$users_dir/*"));

if (defined param("submit")){
    $username = param("username");
    $username =~ s/^\s+|\s+$//g;
    $temp = $username;
    $username = "zid=".$username;
    
    my $flag=0;
    $user = "dataset-medium/$temp";

	foreach (@users) {
		if ($_ =~ ($user)){
		    $flag =1;
		    print error();
	    }
	}
	
	if ($flag ==0){
		$password = param("password");
		$password =~ s/^\s+|\s+$//g;
		$password = "password=".$password;

		$email = param("email");
		$temp2 = $email;
		$email =~ s/^\s+|\s+$//g;
		$email = "email=".$email;

		$full_name = param("full_name");
		$full_name =~ s/^\s+|\s+$//g;
		$full_name = "full_name=".$full_name;

		$program = param("program");
		$program =~ s/^\s+|\s+$//g;
		$program = "program=".$program;

		$birthday = param("birthday");
		$birthday =~ s/^\s+|\s+$//g;
		$birthday = "birthday=".$birthday;

		$home_suburb = param("home_suburb");
		$home_suburb =~ s/^\s+|\s+$//g;
		$home_suburb = "home_suburb=".$home_suburb;

		$courses = param("courses");
		$courses =~ s/^\s+|\s+$//g;
		$courses = "courses=[".$courses;
		$courses = $courses."]";


        chdir "dataset-medium/";
		mkdir $temp unless -d $temp;
		chdir $temp;


		my $user_filename = "dataset-medium/$temp";
		open( my $fh, '>', 'user.txt' ) or die "Can't open 'user.txt'\n";     

		print {$fh} $username."\n";
		print {$fh} $password."\n";
		print {$fh} $email."\n";
		print {$fh} $full_name."\n";

		print {$fh} $program."\n";

		print {$fh} $birthday."\n";

		print {$fh} $home_suburb."\n";

		print {$fh} $courses."\n";
		close $fh;

		`printf " \nLink to your profile : http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$temp\n" | /usr/sbin/sendmail $temp2`;

	 	print "<h1 style=\"text-align:center;\">Check your email!!</h1>",
				 "<div class=\"container_nxt\">",
		        	"<p><a href=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/matelook.cgi\" class=\"btn btn-info btn-sm\">",
		            "<span class=\"glyphicon glyphicon-new-window\"></span>Go back to Login Page</a>",
		        	"</p>",
		      	"</div>";

	}
}   

sub error{
    print "<div class=\"alert alert-danger\" role=\"alert\">",
			"<h1>Error!! Username already exists!</h1></div>\n";
}



        print "<div class=\"container\" style='padding-top: 0px; color: rgb(106,150,242); '>\n",
             	  "<form class=\"form-signin\" role=\"form\" method='POST'>\n",
                    "<h1 class=\"form-signin-heading\">Enter your details...</h1>\n" ,
                      "<input type=\"text\" class=\"form-control\" placeholder=\"Username\" name='username' required=\"autofocus\">\n",'<p><p>',
                      "<input type=\"text\" class=\"form-control\" placeholder=\"Password\" name='password' required>\n",'<p>',
		        "<input type=\"text\" class=\"form-control\" placeholder=\"Email\" name='email' required>\n",'<p>',
		        "<input type=\"text\" class=\"form-control\" placeholder=\"Full Name\" name='full_name' required>\n",'<p>',
		        "<input type=\"text\" class=\"form-control\" placeholder=\"Program\" name='program' required>\n",'<p>',
		        "<input type=\"text\" class=\"form-control\" placeholder=\"Birthday\" name='birthday' required>\n",'<p>',
		        "<input type=\"text\" class=\"form-control\" placeholder=\"Home Suburb\" name='home_suburb' required>\n",'<p>',
		        "<input type=\"text\" class=\"form-control\" placeholder=\"Courses\" name='courses' required>\n",'<p>',
        "<button class=\"btn btn-lg btn-primary btn-block\" type=\"submit\" name='submit'>Submit</button>\n",
              	   "</form></div>\n";
              	   
        print page_trailer();



sub page_trailer {
    print "<marquee behavior=\"alternate\">COMP2041 Assignment 2 by Supratik Baksi- z5081777</marquee>";
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}


