from django.contrib import admin

from .models import Target, Evidence, Country, MemberCharacteristic, Support, Purpose, GovernmentLink, PGAG, Operation, TermType, UCDP, Ethnic, GovernmentCreator, RelativeBenefit, TypeViolence

class TargetOptions(admin.ModelAdmin):
    list_display = ('type',)
    list_filter = ('type',)

class OperationOptions(admin.ModelAdmin):
    list_display = ('group', 'year', 'incidents')
    list_filter = ('group', 'year', 'incidents')

class EvidenceOptions(admin.ModelAdmin):
    list_display = ('group', 'date', 'source')
    list_filter = ('group', 'date')

class CountryOptions(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'code')
    ordering = ('name',)
    search_fields = ('name',)
    
class SupportOptions(admin.ModelAdmin):
    list_display = ('type',)

class MemberCharacteristicOptions(admin.ModelAdmin):
    list_display = ('name',)

class TermTypeOptions(admin.ModelAdmin):
    list_display = ('type',)

class UCDPOptions(admin.ModelAdmin):
    list_display = ('type',)

class EthnicOptions(admin.ModelAdmin):
    list_display = ('type', 'cowgroupid',)

class PurposeOptions(admin.ModelAdmin):
    pass

class GovernmentLinkOptions(admin.ModelAdmin):
    pass

class RelativeBenefitOptions(admin.ModelAdmin):
    pass

class TypeViolenceOptions(admin.ModelAdmin):
    pass

# admin.site.register(GovernmentCreator, GovernmentCreatorOptions)

class PGAGOptions(admin.ModelAdmin):
    filter_vertical = ('successor_group',
                       'predecessor_group',
                       'government_link',
                       'government_creator',
                       'target', 'support_types', 'supporters',
                       'prior_ucdp', 'post_ucdp',
                       'ethnic_targ', 'ethnic_mem', 'ethnic_purp',
                       'membership', 'purpose', 'termination_types',
                       'relative_benefit', 'type_violence')
    fieldsets = (
        ('Basic Identification', 
         {'fields': ('country',
                     'name',
                     'madeup',
                     'date_formed',
                     'accuracy_formed',
                     'date_dissolved',
                     'accuracy_dissolved',
                     'predecessor_group',
                     'prior_group',
                     'prior_armed',
                     'prior_rebel',
                     'prior_ucdp',
                     'successor_group',
                     'post_rebel',
                     'post_ucdp',
                     'pmc')
          }),
        ('Links to Government', 
         {'fields': ('government_relation',
                     'government_link',
                     'party_id',
                     'gov_formed',
                     'government_creator',
                     'target', 
                     'government_trained', 
                     'information_shared',
                     'personnel_shared',
                     'support_types',
                     'supporters',
                     'other_connection')
          }),
          ('Ethnic Characteristics', 
         {'fields': ('ethnic_targ',
                     'info_ethnic_targ',
                     'ethnic_mem',
                     'info_ethnic_mem',
                     'ethnic_purp',
                     'info_ethnic_purp')
          }),
        ('Characteristics', 
         {'fields': ('location',
                     'headcount_low',
                     'headcount_high',
                     'size',
                     'membership',
                     'primary_mem',
                     'alt_primary_mem',
                     'reason_membership',
                     'members_coerced',
                     'members_paid',
                     'members_killed',
                     'origin',
                     'termination_types',
                     'termination',
                     'purpose',
                     'other',
                     'purpose_text',
                     'relative_benefit',
                     'organisation',
                     'weapon_training')
          }),
        ('Treatment of Civilians',
         {'fields': ('treatment_civilians',
                     'type_violence')
          }),
        ('References for Meta-Analysis',
         {'fields': ('reference_meta',)
          }),
        ('Coding progress',
         {'fields': ('finished',)
          }),
        )

    list_display = ('name', 'country')
    ordering = ('country',)
    list_filter = ('purpose',
                   'target',
                   'membership',
                   'support_types',
                   'pmc', 
                   'government_relation',
                   'termination_types')
    search_fields = ('name',)
    
    
admin.site.register(Target, TargetOptions)
admin.site.register(Operation, OperationOptions)
admin.site.register(Evidence, EvidenceOptions)
admin.site.register(Country, CountryOptions)
admin.site.register(Support, SupportOptions)
admin.site.register(MemberCharacteristic, MemberCharacteristicOptions)
admin.site.register(TermType, TermTypeOptions)
admin.site.register(UCDP, UCDPOptions)
admin.site.register(Ethnic, EthnicOptions)
admin.site.register(Purpose, PurposeOptions)
admin.site.register(GovernmentLink, GovernmentLinkOptions)
admin.site.register(PGAG, PGAGOptions)
admin.site.register(TypeViolence, TypeViolenceOptions)
admin.site.register(RelativeBenefit, RelativeBenefitOptions)

# admin.site.register(GovernmentCreator, GovernmentCreatorOptions)
    

