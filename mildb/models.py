from django.db import models
		
class Operation(models.Model):
	YEARRANGE = (("1981","1981"),
		     ("1982","1982"),
		     ("1983","1983"),
		     ("1984","1984"),
		     ("1985","1985"),
		     ("1986","1986"),
		     ("1987","1987"),
		     ("1988","1988"),
		     ("1989","1989"),
		     ("1990","1990"),
		     ("1991","1991"),
		     ("1992","1992"),
		     ("1993","1993"),
		     ("1994","1994"),
		     ("1995","1995"),
		     ("1996","1996"),
		     ("1997","1997"),
		     ("1998","1998"),
		     ("1999","1999"),
		     ("2000","2000"),
		     ("2001","2001"),
		     ("2002","2002"),
		     ("2003","2003"),
		     ("2004","2004"),
		     ("2005","2005"),
		     ("2006","2006"),
		     ("2007","2007"),
		     ("2008","2008"),
		     ("2009","2009"),
		     ("2010","2010"),
		     ("2011","2011"),
		     ("2012","2012"),
		     ("2013","2013"),
             ("2014","2014"),
             ("2015","2015"),)
	year = models.CharField("Year",
				choices=YEARRANGE,
				default="1981",
				max_length=4)
	group = models.ForeignKey("PGAG", on_delete=models.PROTECT)
	incidents = models.IntegerField("Number of incidents")
	
	def __unicode__(self):
		return "%s in %s" % (self.group, self.year)

class Target(models.Model):
	type = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.type


class Evidence(models.Model):
	source = models.CharField("Publication", 
				  max_length=300) 
	date = models.DateField(help_text="Please use the following format: YYYY-MM-DD.")
	group = models.ForeignKey("PGAG",
				  blank=True,
				  null=True,
				  related_name="backing",
                  on_delete=models.PROTECT)
	quote = models.TextField(max_length=1500)
	
	class Meta:
        	verbose_name = 'piece of evidence'
        	verbose_name_plural = 'pieces of evidence'
		
	def __unicode__(self):
		return "%s %s on %s" % (self.source, self.date, self.group)


class Country(models.Model):
	LEVEL1REGION = (('Asia', 'Asia'),
			('Africa','Africa'),
			('Americas','Americas'),
			('Oceania', 'Oceania'),
			('Europe', 'Europe'))
	
	LEVEL2REGION = (('Eastern Africa','Eastern Africa'),
			('Middle Africa','Middle Africa'),
			('Northern Africa','Northern Africa'),
			('Southern Africa','Southern Africa'),
			('Western Africa','Western Africa'),
			('Caribbean', 'Caribbean'),
			('Central America','Central America'),
			('South America','South America'),
			('Northern America','Northern America'),
			('Central Asia','Central Asia'),
			('Eastern Asia','Eastern Asia'),
			('Southern Asia','Southern Asia'),
			('South-Eastern Asia','South-Eastern Asia'),
			('Western Asia','Western Asia'),
			('Eastern Europe','Eastern Europe'),
			('Northern Europe','Northern Europe'),
			('Southern Europe','Southern Europe'),
			('Western Europe','Western Europe'),
			('Australia and New Zealand', 'Australia and New Zealand'),
			('Melanesia','Melanesia'),
			('Micronesia','Micronesia'),
			('Polynesia','Polynesia'))

	name = models.CharField("Name",
				max_length=200)
	abbreviation = models.CharField("Abbreviation",
					max_length=3)
	code = models.IntegerField("Code")

	level1region = models.CharField("Level 1 Region",
					choices=LEVEL1REGION,
					max_length=30,
					default='Africa')

	level2region = models.CharField("Level 2 Region",
					choices=LEVEL2REGION,
					max_length=30,
					default='Eastern Africa')

	isoalpha2 = models.CharField("Abbrev. (2 letter)",
				          max_length=2,
				          blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
        	verbose_name = 'country'
        	verbose_name_plural = 'countries'


class Support(models.Model):
	type = models.CharField(max_length=200)

	# many-to-many with PGAG

	class Meta:
        	verbose_name = 'type of material support'
        	verbose_name_plural = 'types of material support'

	def __unicode__(self):
		return self.type


class MemberCharacteristic(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

# ## added 07/03/13
class TermType(models.Model):
	type = models.CharField(max_length=200)

	# many-to-many with PGAG

	class Meta:
        	verbose_name = 'Termination Type'
        	verbose_name_plural = 'Termination Types'

	def __unicode__(self):
		return self.type

## added 07/03/13
class UCDP(models.Model):
	type = models.CharField(max_length=200)

	# many-to-many with PGAG

	class Meta:
        	verbose_name = 'UCDP Actor ID'

	def __unicode__(self):
		return self.type


class Purpose(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
        	verbose_name = 'group purpose'

	def __unicode__(self):
		return self.name


class GovernmentLink(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class GovernmentCreator(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name
	
## adding ethnic class: membership, target, purpose

class Ethnic(models.Model):
	type = models.CharField("EPR Name (Country)", max_length=200,
				 help_text="Please enter EPR group name and add country in brackets. Example: Israeli Arabs (Israel)")

	cowgroupid = models.PositiveIntegerField("cowgroupid",
					   blank=True,
					   null=True,
					   default=0,
					   help_text="Please provide EPR cowgroupid")

	# many-to-many with PGAG

	class Meta:
            verbose_name = 'Ethnic Group (EPR)'
            verbose_name_plural = 'Ethnic Groups (EPR)'

	def __unicode__(self):
		return self.type



class RelativeBenefit(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name


class TypeViolence(models.Model):
	name = models.CharField(max_length=100)

	class Meta:
        	verbose_name = 'type of violence'
        	verbose_name_plural = 'types of violence'

	def __unicode__(self):
		return self.name




class PGAG(models.Model):

	YNUN = (('noinf', 'no information'),
		('yes', 'yes'), 
		('no', 'no'), 
		('unclear', 'unclear'))

## YNUN2 includes the option N/A
	YNUN2 = (('noinf', 'no information'),
		('yes', 'yes'), 
		('no', 'no'), 
		('unclear', 'unclear'),
        ('NA', 'NA'))

## YNUN3 only gives yes no options
	YNUN3 = (('yes', 'yes'),
		('no', 'no'))
	
	ACC = (('dec', 'decade'),
		('yr', 'year'), 
		('mo', 'month'), 
		('dy', 'day'))

	GOVREL = (('type1or2', 'unclear (type 1 or 2)'),
		  ('type2', 'semi-official (type 2)'),
		  ('type1', 'informal (type 1)'),
		  ('unclear', 'unclear'))

	QUAL = (('giv','given'),
		('inf','inferred'),
		('na','not applicable'))

	MEM = (('noinf','no information'),
		('ethnic','ethnic'),
		('ideological','ideological'),
		('local','local'),
		('nationalist','nationalist'),
		('noncivilian','non-civilian'),
		('political','political'),
		('religious','religious'),
		('other','other'),
		('unclear','unclear'))

	FREQCAT = (('noinf', 'no information'),
		('never', 'never'),
		('rarely', 'rarely'),
		('sometimes', 'sometimes'),
		('often', 'often'),
		('unclear', 'unclear'))

	# Basic identification
	name = models.CharField(max_length=200)
	madeup = models.BooleanField(verbose_name="Name assigned by coder",
				     default=False)
	country = models.ForeignKey(Country, on_delete=models.PROTECT)
	
	date_formed =  models.DateField("Date formed or first mentioned",
					help_text="Please use the following format: YYYY-MM-DD.")
	accuracy_formed = models.CharField("Accuracy of date formed", 
				choices=ACC,
				max_length=30,
				default='dy')
	date_dissolved = models.DateField("Date dissolved", 
					  blank=True, 
					  null=True,
					  help_text="Please use the following format: YYYY-MM-DD.")
	accuracy_dissolved = models.CharField("Accuracy of date dissolved", 
				choices=ACC,
				max_length=30,
				default='dy')
    
	predecessor_group = models.ManyToManyField("self", symmetrical=False,
						 blank=True)
	
	successor_group = models.ManyToManyField("self",symmetrical=False,
						related_name='successors',
						 blank=True)
	# Problem: many to many field relates things symetrical, i.e. changes in both PGMs ("if I am your successor, you are mine")
	# symmetrical = False prevents from doing this
	# Source symmetrical: https://docs.djangoproject.com/en/1.8/ref/models/fields/#django.db.models.ManyToManyField.symmetrical
	prior_group = models.CharField("Former Existing Group?", 
			       choices=YNUN,
			       max_length=30,
			       default='noinf')
	
	prior_armed = models.CharField("Former Armed Group?", 
			       choices=YNUN2,
			       max_length=30,
			       default='NA')
	
	prior_rebel = models.CharField("Former Rebel Group?", 
			       choices=YNUN2,
			       max_length=30,
			       default='NA')
			       
	prior_ucdp = models.ManyToManyField(UCDP, 
				verbose_name="UCDP Actor ID of former rebel group",
				blank=True)
				       
	post_rebel = models.CharField("PGM becomes Rebel Group?", 
				choices=YNUN,
				max_length=30,
				default='noinf')
				       
	post_ucdp = models.ManyToManyField(UCDP, 
				verbose_name="UCDP Actor ID of successor rebel group",
				related_name='prior_group',
				blank=True)

	pmc = models.CharField("PMC", 
			       choices=YNUN,
			       max_length=30,
			       default='noinf')

	
	# Links to government
	
	government_relation = models.CharField("Government relation", 
					       choices=GOVREL,
					       max_length=30,
					       default='type1')
	
	government_link = models.ManyToManyField(GovernmentLink)

	gov_formed = models.CharField("Created by Government?", 
			       choices=YNUN,
			       max_length=30,
			       default='noinf')

	government_creator = models.ManyToManyField(GovernmentCreator,
						    verbose_name="Creating Government Institution",
						    blank=True)
		
	target = models.ManyToManyField(Target,
					blank=True)
	
	party_id = models.CharField("Name of Party Link",
				    max_length=100,
				    help_text="Name of Political Party linked to PGM",
				    blank=True,
				    null=True)
	government_trained = models.CharField(choices=YNUN,
					      max_length=30,
					      default='noinf')
	information_shared = models.CharField("Shared information", 
					      choices=YNUN,
					      max_length=30,
					      default='noinf')
	information_shared = models.CharField("Shared information", 
					      choices=YNUN,
					      max_length=30,
					      default='noinf')
	personnel_shared = models.CharField("Shared personnel", 
					    choices=YNUN,
					    max_length=30,
					    default='noinf')
	support_types =  models.ManyToManyField(Support, 
						verbose_name="Types of material support")
	termination_types = models.ManyToManyField(TermType, 
						verbose_name="Termination Types",
						blank=True)
	supporters = models.ManyToManyField(Country,
					    verbose_name="State sponsors",
					    related_name='sponsors',
					    blank=True)
	other_connection = models.CharField("Other connection", 
					    max_length=400,
					    blank=True)

		# Ethnic Characteristics

	ethnic_targ = models.ManyToManyField(Ethnic,
				verbose_name="Ethnic Target",
				help_text="Select or add EPR Group",
				blank=True)
	
	info_ethnic_targ = models.CharField("Quality of Information for Ethnic Targeting", 
			       choices=QUAL,
			       max_length=30,
			       default='na')
	
	ethnic_mem =  models.ManyToManyField(Ethnic,
			       verbose_name="Ethnic Membership",
			       related_name='ethnic_target',
			       blank=True,
			       help_text="Select or add EPR Group")
	
	info_ethnic_mem = models.CharField("Quality of Information for Ethnic Membership", 
				choices=QUAL,
			       max_length=30,
			       default='na')
	
	ethnic_purp =  models.ManyToManyField(Ethnic,
				verbose_name="Ethnic Purpose",
				related_name='ethnic_mem',
				blank=True,
				help_text="Select or add EPR Group")

	info_ethnic_purp = models.CharField("Quality of Information for Ethnic Purpose", 
			       choices=QUAL,
			       max_length=30,
			       default='na')

	# Characteristics of PAGs

	location = models.CharField(max_length=200,
				    help_text="Primary location of activities",
				    blank=True,
				    null=True)
	headcount_low = models.PositiveIntegerField("Minimum headcount",
						    blank=True,
						    null=True)
	headcount_high = models.PositiveIntegerField("Maximum headcount",
						     blank=True,
						     null=True)
	membership = models.ManyToManyField(MemberCharacteristic)
	origin = models.TextField(max_length=500, 
				  blank=True)
	termination = models.TextField(max_length=500,
				       blank=True)
	purpose = models.ManyToManyField(Purpose)
	other = models.TextField(max_length=1000,
				 blank=True)

    ### new variables for meta analysis
	forced_mem = models.CharField("Forced Membership",
			       choices=QUAL,
			       max_length=30,
			       default='na')

	### new June 2016
	primary_mem = models.CharField("Primary Membership",
					choices=MEM,
					max_length=30,
					default = 'noinf')

	alt_primary_mem = models.CharField("Alternative Primary Membership",
					choices=MEM,
					max_length=30,
					default = 'noinf')

	## new January 2018

	purpose_text = models.TextField("Purpose",
					max_length=1000,
				 	blank=True)
	relative_benefit = models.ManyToManyField(RelativeBenefit,blank=True, verbose_name="Relative Benefit")
	treatment_civilians =  models.TextField("Treatment of Civilians",
					max_length=1000,
					blank=True)
	type_violence = models.ManyToManyField(TypeViolence, verbose_name="Types of Violence", blank=True)
	members_killed = models.CharField(choices=FREQCAT,
					      max_length=30,
					      default='noinf')
	members_coerced = models.CharField(choices=YNUN,
					      max_length=30,
					      default='noinf')
	members_paid = models.CharField("Members paid",
						  choices=YNUN,
					      max_length=30,
					      default='noinf')
	size = models.TextField("Size",
							max_length=1000,
				 			blank=True)
	weapon_training = models.TextField("Weapons and Training",
							max_length=1000,
				 			blank=True)
	organisation = models.TextField("Organisation",
							max_length=1000,
				 			blank=True)

	## new 22.Feb.18
	reason_membership = models.TextField("Reasons for Membership",
					max_length=1000,
				 	blank=True)

	## new 09.March.18: Field for references meta-analysis
	reference_meta = models.TextField("References for Meta-Analysis",
					max_length=10000,
					help_text="Please add references in alphabetical order and insert an empty line after each reference.",
				 	blank=True)

	## new 09.01.19: Field if coding is finished
	finished = models.CharField("Coding completed",
						  choices=YNUN3,
					      max_length=30,
					      default='no')


#    purpose_details = models.TextField("Details of group purpose", 
# 			       max_length=1000,
# 			       blank=True)  
#    purpose_successful = models.TextField("Was the purpose successfully fulfilled?", max_length=1000,
#				 blank=True)
#    additional_names = models.TextField("Additional group names", max_length=1000,
#				 blank=True)
#    conseq_gov = models.TextField("Consequences for government", max_length=1000,
#				 blank=True)
#    conseq_pgm = models.TextField("Consequences for PGM", max_length=1000,
#				 blank=True)
#    conseq_pop = models.TextField("Consequences for civilian population", max_length=1000,
#				 blank=True)

	
	# evidence here?

	def __unicode__(self):
		return "%s (%s)" % (self.name, self.country)

	class Meta:
        	verbose_name = 'PGM'
        	verbose_name_plural = 'PGMs'

