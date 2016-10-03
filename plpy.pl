#!/usr/bin/perl -w

#use strict;


# Assignment 2 'plpy.pl' written by Supratik Baksi, z5081777

my $whiteSpaces = 0; # to keep the count of the number of white spaces
# try adding a loop counter to add or subtract for spaces
my $loopCounter =0;
# to count the number of white spaces in every line to be printed
my $flag = 0;
sub printWhiteSpaces {
	my $whitespace = $_[0];
	for (my $i = 0; $i < $whitespace; $i++) {
		print '    ';  
	}
}
# my $sys = 0;
# my $fileinput = 0;
# my @code = <>

# foreach $line (@code) {
#	if($line =~ /<STDIN>/ || $line =~ /ARGV/){	
#		$sys = 1;
#		$line =~ s/\@ARGV/sys.argv[1:]/g;	
#	}
#	if($line =~ /(\d)+\.\.(\d)+/){
#	    $range1 = $1;
#	    $range2 = $2+1;
#	    $line =~ s/\d+\.\.\d+/range($range1, $range2)/g;
#	}
#	if($line =~ /<>/){
#	    $fileinput = 1;
#	}
#}

#foreach my $line (@code) {
while (my $line = <>) {
# to translate #! line 
	if ($line =~ /^#!/ && $. == 1){ 
		print "#!/usr/local/bin/python3.5 -u\n"; 
		#if ($sys){
			# stdin / @ARGV case
		#	print "import sys\n";
		#	$sys = 0;
		#}
		#if ($fileinput){
		   #fileinput case
		 #  print "import fileinput, re\n";
		  # $fileinput = 0;
		#}	
#	}

# for fileinput
	} elsif ($line =~ /^\s*while\s*(.*)\<\>(.*)\s*(.*)\s*$/) {
		&printWhiteSpaces($whiteSpaces);	
		print "import fileinput, re\n";
		&printWhiteSpaces($whiteSpaces);	
		print "for line in fileinput.input():\n"	

# for STDIN
	} elsif ($line =~ /^\s*while\s*(.*)\<STDIN\>(.*)\s*(.*)\s*$/) {
		&printWhiteSpaces($whiteSpaces);
		print "import sys\n";
		&printWhiteSpaces($whiteSpaces);
		print "for line in sys.stdin:\n"; 
# to deal with blank & comment lines
	} elsif ($line =~ /^\s*#/ || $line =~ /^\s*$/) {
		print $line;
		
# to deal with print statements with \n
	} elsif ($line =~ /^\s*print\s*"(.*)\\n"[\s;]*$/) { 
		my $var = $1; # var = unknown variable
		if($var =~ /ARGV\[(.*)\]$/) { # the variable is ARGV[] 
			&printWhiteSpaces($whiteSpaces);
			my $argument = $1; 
			$argument =~ s/\$//g; # remove variable sign from argument
			$argument =~ s/my//;
			print "print (sys.argv[$argument + 1])\n"
			
		} elsif ($var =~ /^(.*)\s*\$(.*)*$/) { #there is one variable
			$var =~ s/\$//g; #removes variable signs
			$var =~ s/my//;
			&printWhiteSpaces($whiteSpaces);
			print "print ($var)\n";
			
		} elsif ($var =~ /^(.*)\s*\@(.*)*$/) { #there is one array variable
			$var =~ s/\@//g;
			$var =~ s/my//;
			&printWhiteSpaces($whiteSpaces);
			print "print ($var)\n";
			
		} else { # for when there is no variable
			&printWhiteSpaces($whiteSpaces);
			print "print (\"$var\")\n";
		}

# to deal with print statements with \n (special case of stuff outside "")
	} elsif ($line =~ /^\s*print\s*(.*)\s*"(.*)\\n"[\s;]*$/) {
		my $var = $1; # var = unknown variable
		if ($var =~ /^(.*)\s*\$(.*)*$/) { #there is one variable
			$var =~ s/\$//g; #removes variable signs
			$var =~ s/my//;
			$var =~ s/\,//;			
			&printWhiteSpaces($whiteSpaces);
		

# to deal with join
	    } if($var =~ /join\s*\((.*)\s*,\s*(.*)\)/){
			my $char = $1;
			my $join = $2;
			$var =~ s/join\s*\(.*\)/$char.join($join)/g;
			$var =~ s/,*\s*\"\\n\";//g;
			# ARGV case
			if($line =~ /ARGV/){
			    &printWhiteSpaces($whiteSpaces);
		        print "import sys\n";
			}
			$var =~ s/\@ARGV/sys.argv[1:]/g;
			$var =~ s/\,//g;			
			}
		print "print ($var)\n";
# to deal with print statments without \n
	} elsif ($line =~ /^\s*print\s*"(.*)"[\s;]*$/) { # multiple \s's as there can be random spaces between the words
		my $var = $1;
		if ($var =~ /^\s*print\s*\$\_\s*;$/) { #special case for $_ i.e. incase outputing var from cmd line
			&printWhiteSpaces($whiteSpaces);		
			print "print line\n";
			
		} elsif ($var =~ /^(.*)\s*\$(.*)*$/) { #there is ONE variable
			&printWhiteSpaces($whiteSpaces);
			$var =~ s/my//;			
			$var =~ s/[\$\@]//g; #removes variable signs
			print "sys.stdout.write($var)\n";

		} else { #there is no variable 
			&printWhiteSpaces($whiteSpaces);
			print "sys.stdout.write(\"$var\")\n";
		}
# to deal with arithmetic operations
	} elsif ($line =~ /^\s*[^\s]*\s*=(.*);$/) {
		if ($line =~ /^\s*\@(.*)\s*=\s*(.*);$/) { # deal with arrays separately
			next;
		} else {
			&printWhiteSpaces($whiteSpaces-$loopCounter);
			&arithmeticLines($line);
		}
sub arithmeticLines { 

	# $#
	$_[0] =~ s/\$\#ARGV/len\(sys\.argv\)/;

    if($_[0] =~ /(\w+)\s*([><=!%]+)\s*(\d+)\s*/){ # case for when STDIN is a number
        $_[0] =~ s/($1)/float\($1\)/;
    }
    if($_[0] =~ /float\((\w+)\)\s*(=)\s*(\d+)\s*/){# case to not match basic initialisation
        $_[0] =~ s/float\(($1)\)/$1/;    
    }
	# removes $,@, my
	$_[0] =~ s/\$//g;
	$_[0] =~ s/\@//g;
	$_[0] =~ s/my//;

	# STDIN
	if($_[0] =~ /<STDIN>/ && $flag == 0){
		    &printWhiteSpaces($whiteSpaces);
		    print "import sys\n";
		    $flag = 1;
		    $_[0] =~ s/\<STDIN\>/sys\.stdin\.readline\(\)/;
		    }
    
	  
	#$string =~ s/(\$\w+)\s*([><=!]+)\s*(\d+)\s*(?=:)/float($1) $2 $3/;
	       
	# and/or/not
	$_[0] =~ s/\&\&/and /g;
	$_[0] =~ s/\|\|/or /g;
	$_[0] =~ s/!\s/not /g;

	# comparison operators 
	$_[0] =~ s/ eq / == /g;
	$_[0] =~ s/ ne / != /g;
	$_[0] =~ s/ gt / > /g;
	$_[0] =~ s/ lt / < /g;
	$_[0] =~ s/ ge / >= /g;
	$_[0] =~ s/ le / <= /g;	

	# division
	$_[0] =~ s/\//\//g;

	# remove semicolon
	$_[0] =~ s/\;//;
	print $_[0];
}
# to deal with comparison stuff
	} elsif ($line =~ /^\s*while\s*\(([^(^).]*)\)\s*$/){
		$line =~ s/[\(\$]//g;
		$line =~ s/\)\s*{/:/g;
		$line =~ s/eq/==/g;
		$line =~ s/lt/</g;
		$line =~ s/gt/>/g;
		$line =~ s/le/<=/g;
		$line =~ s/ge/>=/g;
		$line =~ s/ne/!=/g;
		&printWhiteSpaces($whiteSpaces);
        print $line;
	
		
# to deal with break/continue	
	} elsif ($line =~ /^\s*last;$/) {
		&printWhiteSpaces($whiteSpaces +1); 
		print "break\n";
		
	} elsif ($line =~ /^\s*next;$/) {
		&printWhiteSpaces($whiteSpaces);
		print "continue\n";

# to deal with chomp
	} elsif ($line =~ /^\s*chomp\s*\$(.*)\s*;$/) {
		&printWhiteSpaces($whiteSpaces - $loopCounter);
		$variable = $1;
		$line =~ s/[^\s].*//g;
		chomp $line;
		print "$line$variable = $variable.rstrip()\n"
		
# to deal with split
	} elsif ($line =~ /^\s*(.*)\s*=\s*split\(\/(.*)\/,\s*\$(.*)\)\s*;/) {
		$line =~ s/\$//g;
		$line =~ s/\@//g;
		$line =~ s/my//;
		my $string = $3;
		my $delimeter = $2;
		my $variable = $1;
		&printWhiteSpaces($whiteSpaces);
		print "$variable = $string.split(\"$delimeter\")\n";


# to deal with ++ and --
	} elsif ($line =~ /(\s*)(\$.*)\+\+|(.*)--/){
		&printWhiteSpaces($whiteSpaces);
		$line =~ s/\$//g;
		$line =~ s/my//;
		$line =~ s/\+\+\s*;/ += 1/g;
		$line =~ s/--\s*;/ -= 1/g;
		print $line;



# to deal with foreach
	} elsif ($line =~ /^\s*foreach\s*\$(.*)\s*\((.*)\)\s*{\s*$/) {
		&printWhiteSpaces($whiteSpaces);
		# to deal with specific case of range
		if($line =~ /(\d)+\.\.(\d)+/){
	    		my $val1 = $1;
 			my $val2 = $2+1;
    			$line =~ s/\d+\.\.\d+/range($val1, $val2)/g;
		}
		# to deal with the specific case of range where end is $#ARGV
		if($line =~ /0\.\.\$#ARGV/){
		        $line =~ s/0\.\.\$#ARGV/range(len(sys.argv)-1)/g;
		        $flag = 2;
 		}
		$line =~ s/each*|\$*//g;
		$line =~ s/\(/in /;
		$line =~ s/\)\s*{/:/g;
		$line =~ s/my//;
		$line =~ s/\@//g;
		if($line =~ /ARGV/){
		    &printWhiteSpaces($whiteSpaces);
		    print "import sys\n";
		}
		$line =~ s/ARGV/sys.argv[1:]/g;
			
		$whiteSpaces ++;
		if($flag == 2){
		    print "import sys\n";
		}
		print "$line";


# to deal with while loops
	} elsif ($line =~ /^\s*(.*)\s*while\s*\((.*)\)(.*)\s*$/) {
	    $loopCounter ++;
		if ($line =~ /^\s*(.*)\s*while\s*\((.*)\s*\<STDIN\>\s*\)(.*)\s*$/) { # STDIN condition
			&printWhiteSpaces($whiteSpaces);		
			print "for line in sys.stdin:";
			$whiteSpaces ++;
		} else {
			my $condition = $2;
			&printWhiteSpaces($whiteSpaces);		
			print "while ";
			&arithmeticLines($condition);
			print ":\n";
			$whiteSpaces ++;
		}

# to deal with elsif 
	} elsif ($line =~ /^\s*(.*)\s*elsif\s*\((.*)\)(.*)\s*$/) {
		my $condition = $2;
		&printWhiteSpaces($whiteSpaces-1);
		print "elif ";		
		&arithmeticLines($condition);
		print ":\n";

# to deal with if statements
	} elsif ($line =~ /^\s*(.*)\s*if\s*\((.*)\)(.*)\s*$/) {
		my $condition = $2;
		&printWhiteSpaces($whiteSpaces);
		print "if ";	
		&arithmeticLines($condition);
		print ":\n";
		$whiteSpaces ++;

# to deal with else
	} elsif ($line =~ /^\s*(.*)\s*else\s*(.*)\s*$/) {
		&printWhiteSpaces($whiteSpaces-1);
		print "else:\n";

# to end curly brace
	} elsif ($line =~ /^\s*}\s*$/) {
		$line =~ s/\}/ /;
		$whiteSpaces --;

# to deal with array conversion
	}elsif ($line =~ /^\s*(.*)\s*\@(.*)\s*(.*)\s*;$/) { # array in the line	
		my $arrayName = $2; 
		if (/^\s*(.*)\s*\@(.*)\s*=\s*((.*))\s*;$/) { # declaring the array
			$line =~ s/\@//;
			$line =~ s/my//;
			$line =~ s/\(/\[/;
			$line =~ s/\)/\]/;
			$line =~ s/\"/\'/g;
			$line =~ s/\;//;
			print "$line";
		} else { # accessing the array
			$line =~ s/\@//;
			$line =~ s/my//;
			$line =~ s/\;//;
			print "$line";
		}
#to deal with push
	} elsif ($line =~ /^\s*push\s*\@(.*)\,\s*(.*)\s*;$/) {
		&printWhiteSpaces($whiteSpaces);
		print "$1.push($2)\n";

# to deal with pop
	} elsif ($line =~ /^\s*pop\s*\@(.*);$/) {
		&printWhiteSpaces($whiteSpaces);
		print "$1.pop\n";

# to deal with unshift
	} elsif ($line =~ /^\s*unshift\s*\@(.*)\,\s*(.*)\s*;$/) {
		&printWhiteSpaces($whiteSpaces);
		print "$1.unshift($2)\n";

# to deal with shift
	} elsif ($line =~ /^\s*shift\s*\@(.*);$/) {
		&printWhiteSpaces($whiteSpaces);
		print "$1.shift\n";

# to translate 's///' command
	} elsif ($line =~ /(.*)\s*=~\s*s\/(.*)\/(.*)\/g*;/){
	        my $variable = $1;
	        my $phrase = $2;
	        my $replace = $3;
	  	    $line =~ s/[\$;]//g;
	  	    #$line =~ s/~\s*s\/.*\/.*\/g*/ re.sub(r'$phrase', '$replace', $variable)/g;
	    	print "$variable = re.sub(r'$phrase', '$replace', $variable)";
	    	$whiteSpaces ++;
	    	print "++++++++++++++";
# to deal with hash tables
	} elsif ($line =~ /^\s*\$[^\s]*{(.*)}\s*=\s*(.*);/){

		$line =~ s/\$//g;
		$line =~ s/{/[/g;
		$line =~ s/}/]/g;
		print $line;
    
# Could not translate -> comments
	} else { 
		print "#$line\n";
	}

}

