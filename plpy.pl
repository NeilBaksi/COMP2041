#!/usr/bin/perl -w

use strict;

# Assignment 2 'plpy.pl' written by Supratik Baksi, z5081777

my $whiteSpaces = 0; # to keep the count of the number of white spaces

# to count the number of white spaces in every line to be printed
sub printWhiteSpaces {
	my $whitespace = $_[0];
	for (my $i = 0; $i < $whitespace; $i++) {
		print '   ';  
	}
}
foreach my $line (<>) {
    # skim read to set flags and translating certain phrases
	if($line =~ /<STDIN>/ || $line =~ /ARGV/){	
		$sys = 1;
		$line =~ s/\@ARGV/sys.argv[1:]/g;
	}
	if($line =~ /(\d)+\.\.(\d)+/){
	    $range1 = $1;
	    $range2 = $2+1;
	    $line =~ s/\d+\.\.\d+/xrange($range1, $range2)/g;
	}
	if($line =~ /<>/){
	    $fileinput = 1;
	}
	if($line =~ /0\.\.\$#ARGV/){
	    $line =~ s/0\.\.\$#ARGV/xrange(len(sys.argv)-1)/g;
	}
	if($line =~ /\$ARGV\[(.*)\]/){
	    $index = $1;
	    $index =~ s/\$//g;
	    $line =~ s/ARGV\[.*\]/sys.argv[$index+1]/g;
	}
	if($line =~ /(\$[^\s]*)\s*%|[<>=]+\s*[\d]+/){
	    $float = 1;
	    $floatvariable = $1;    
    }
    if($line =~ /open\s(.*),\s*[\"<>]*([^";]*)[\";]*/){
		$open{$1} = $2;
    }
    if($line =~ /\$([^\s]*){.*}.*;/g){
		$hash = 1;
		$hashes{$1} = 1;
    }
    if($line =~ /\$[1-9]/){
		$line =~ s/\$([0-9])/m.group($1)/g;
    }
}

while ($line = <>) {

# to translate #! line 
	if ($line =~ /^#!/ && $. == 1){ 
		print "#!/usr/bin/python3.5 -u\n"; 
		
# to deal with blank & comment lines
	} elsif ($line =~ /^\s*#/ || $line =~ /^\s*$/) {
		print $line;
		
# to deal with variable initialization
	#} elsif ($line =~ /^\s*(my)*\s*\$([\w\d]*)\s*=\s*([^;^~]*)[\s;]*$/){
	#	my $content = $3;
	#	$line =~ s/[\$;]//g;
	#	if ($content eq "<STDIN>"){
	#	    # <STDIN> case
	#		$line =~ s/<STDIN>/sys.stdin.readline()/g;			 
	#	    if($float){
         #       $line =~ s/=\s*/= float(/g;
          #      $line =~ s/\n/)\n/g;
         #   }
	#	}
	#	print $line; 	

# to deal with print statements with \n
	} elsif ($line =~ /^\s*print\s*"(.*)\\n"[\s;]*$/) { 
		my $var = $1; # var = individual line, the part b/w print and \n 
		if($var =~ /ARGV\[(.*)\]$/) { #the variable is ARGV[] 
			&printWhiteSpaces($whiteSpaces);
			my $argument = $1; 
			$argument =~ s/\$//; # remove variable sign from argument
			print "print sys.argv[$argument + 1]\n"
			
		} elsif ($var =~ /^(.*)\s*\$(.*)*$/) { #there is one variable
			$var =~ s/\$//; #removes variable signs
			&printWhiteSpaces($whiteSpaces);
			print "print $var\n";
			
		} elsif ($var =~ /^(.*)\s*\@(.*)*$/) { #there is one array variable
			$var =~ s/\@//;
			&printWhiteSpaces($whiteSpaces);
			print "print $var\n";
		} else { #there is no variable
			&printWhiteSpaces($whiteSpaces);
			print "print \"$var\"\n";
		}

# to deal with print statments without \n
	} elsif ($line =~ /^\s*print\s*"(.*)"[\s;]*$/) { # multiple \s's as there can be random spaces between the words
		my $var = $1;
		if ($var =~ /^\s*print\s*\$\_\s*;$/) { #special case for $_ i.e. incase outputing var from cmd line
			&printWhiteSpaces($whiteSpaces);		
			print "print line\n";
			
		} elsif ($var =~ /^(.*)\s*\$(.*)*$/) { #there is ONE variable
			&printWhiteSpaces($whiteSpaces);			
			$var =~ s/[\$\@]//; #removes variable signs
			# $var =~ s/\@//;
			print "sys.stdout.write($var)\n";
			
		} else { #there is no variable 
			&printWhiteSpaces($whiteSpaces);
			print "sys.stdout.write(\"$var\")\n";
		}
# to deal with arithmetic operations
	} elsif ($line =~ /^\s*[^\s]*\s*=(.*);$/) {
		if ($line =~ /^\s*\@(.*)\s*=\s*(.*);$/) {#arrays are dealt with seperately
			next;
		} else {
			&printWhiteSpaces($whiteSpaces);
			&arithmeticLines($line);
		}
sub arithmeticLines { 

	# $#
	$_[0] =~ s/\$\#ARGV/len\(sys\.argv\)/;

	#removes $
	$_[0] =~ s/\$//g;
	$_[0] =~ s/\@//g;

	#stdin
	$_[0] =~ s/\<STDIN\>/float\(sys\.stdin\.readline\(\)\)/;

	#and/or/not
	$_[0] =~ s/\&\&/and /g;
	$_[0] =~ s/\|\|/or /g;
	$_[0] =~ s/!\s/not /g;

	#comparison operators 
	$_[0] =~ s/ eq / == /g;
	$_[0] =~ s/ ne / != /g;
	$_[0] =~ s/ gt / > /g;
	$_[0] =~ s/ lt / < /g;
	$_[0] =~ s/ ge / >= /g;
	$_[0] =~ s/ le / <= /g;	

	#division
	$_[0] =~ s/\//\/\//g;

	#remove semicolon
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
		
#looping through every line in a FILE 
	} elsif ($line =~ /^\s*while\s*(.*)\<\>(.*)\s*(.*)\s*$/) {
		&printWhiteSpaces($whiteSpaces);	
		print "import fileinput\n";
		&printWhiteSpaces($whiteSpaces);	
		print "for line in fileinput.input():\n"	

#looping through STDIN (while loop)
	} elsif ($line =~ /^\s*while\s*(.*)\<STDIN\>(.*)\s*(.*)\s*$/) {
		&printWhiteSpaces($whiteSpaces);
		print "import sys\n";
		&printWhiteSpaces($whiteSpaces);
		print "for line in sys.stdin:\n"; 
		
# to deal with break/continue	
	} elsif ($line =~ /^\s*last;$/) {
		&printWhiteSpaces($whiteSpaces);
		print "break\n";
		
	} elsif ($line =~ /^\s*next;$/) {
		&printWhiteSpaces($whiteSpaces);
		print "continue\n";

#chomp from STDIN
	} elsif ($line =~ /^\s*chomp\s*\$(.*)\s*;$/) {
		&printWhiteSpaces($whiteSpaces);	
		print "$1 = sys.stdin.readlines()\n";
		#&printWhiteSpaces($whiteSpaces);
		#print "$1 = $1.rstrip()\n";

#split
	} elsif ($line =~ /^\s*(.*)\s*=\s*split\(\/(.*)\/,\s*\$(.*)\)\s*;/) {
		my $string = $3;
		my $delineator = $2;
		my $assignmentVariable = $1;
		&printWhiteSpaces($whiteSpaces);
		print "$assignmentVariable = $string.split(\"$delineator\")\n";

#join
	} elsif ($line =~ /^\s*(.*)\s*=\s*join\(\'(.*)\'\,\s*(.*)\)\s*;$/) {
		my $assignmentVariable = $1;
		my $string = $3;
		my $delineator = $2;
		&printWhiteSpaces($whiteSpaces);
		print "$assignmentVariable = '$delineator'.join([$string])";

# to deal with ++ and --
	} elsif ($line =~ /(\s*)(\$.*)\+\+|(.*)--/){
		&printWhiteSpaces($whiteSpaces);
		$line =~ s/\$//g;
		$line =~ s/\+\+\s*;/ += 1/g;
		$line =~ s/--\s*;/ -= 1/g;
		print $line;

#foreach (with ARGV) (super specific, could do with broadening in scope)
	} elsif ($line =~ /^\s*foreach\s*\$(.*)\s*\((.*)\)\s*{\s*$/) {
		&printWhiteSpaces($whiteSpaces);
		$line =~ s/each*|\$*//g;
		$line =~ s/\(/in /;
		$line =~ s/\)\s*{/:/g;
		$line =~ s/\@//g;
		print "$line";
#while loops
	} elsif ($line =~ /^\s*(.*)\s*while\s*\((.*)\)(.*)\s*$/) {
		if ($line =~ /^\s*(.*)\s*while\s*\((.*)\s*\<STDIN\>\s*\)(.*)\s*$/) { # STDIN condition
			&printWhiteSpaces($whiteSpaces);		
			print "for line in sys.stdin:";
		} else {
			my $whileCondition = $2;
			&printWhiteSpaces($whiteSpaces);		
			print "while ";
			&arithmeticLines($whileCondition);
			print ":\n";
			$whiteSpaces ++;
		}

# elsif 
	} elsif ($line =~ /^\s*(.*)\s*elsif\s*\((.*)\)(.*)\s*$/) {
		#remember to remove } if present
		#becomes elif
		my $elsifCondition = $2;
		&printWhiteSpaces($whiteSpaces-1);
		print "elif ";					#so, so frustratingly messy :/
		&arithmeticLines($elsifCondition);
		print ":\n";

#if statements
	} elsif ($line =~ /^\s*(.*)\s*if\s*\((.*)\)(.*)\s*$/) {
		my $ifCondition = $2;
		&printWhiteSpaces($whiteSpaces);
		print "if ";					#ugh this is messy :/
		&arithmeticLines($ifCondition);
		print ":\n";
		$whiteSpaces ++;

#else
	} elsif ($line =~ /^\s*(.*)\s*else\s*(.*)\s*$/) {
		#remember to remove } if present
		&printWhiteSpaces($whiteSpaces-1);
		print "else:\n";;

#end curly brace needs removal
	} elsif ($line =~ /^\s*}\s*$/) {
		$line =~ s/\}/ /;
		$whiteSpaces --;

#array conversion
	}elsif ($line =~ /^\s*(.*)\s*\@(.*)\s*(.*)\s*;$/) { #array in the line	
		my $arrayName = $2; 
		if (/^\s*(.*)\s*\@(.*)\s*=\s*((.*))\s*;$/) { #declaring the array
			$line =~ s/\@//;
			$line =~ s/\(/\[/;
			$line =~ s/\)/\]/;
			$line =~ s/\"/\'/g;
			$line =~ s/\;//;
			print "$line";
		} else { #accessing the array
			#  $arrayName[0 or whatever];
			$line =~ s/\@//;
			$line =~ s/\;//;
			print "$line";
		}
#push
	} elsif ($line =~ /^\s*push\s*\@(.*)\,\s*(.*)\s*;$/) {
		&printWhiteSpaces($whiteSpaces);
		print "$1.push($2)\n";

#pop
	} elsif ($line =~ /^\s*pop\s*\@(.*);$/) {
		&printWhiteSpaces($whiteSpaces);
		print "$1.pop\n";

#unshift
	} elsif ($line =~ /^\s*unshift\s*\@(.*)\,\s*(.*)\s*;$/) {
		&printWhiteSpaces($whiteSpaces);
		print "$1.unshift($2)\n";

#pop
	} elsif ($line =~ /^\s*shift\s*\@(.*);$/) {
		&printWhiteSpaces($whiteSpaces);
		print "$1.shift\n";

# Lines we can't translate are turned into comments
	} else { 
		print "#$line\n";
	}

}
