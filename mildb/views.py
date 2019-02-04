from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.db.models import Q
#from django.template import loader
from .models import Country, PGAG, Operation, Evidence, Target, MemberCharacteristic, GovernmentLink, Support, Purpose, TermType, Ethnic, GovernmentCreator, RelativeBenefit, TypeViolence

import csv
import colorsys
from datetime import datetime

def float2dec(color):
    return int(color*255)

def dec2hex_str(rgb):
    return "%06x" % (rgb[0]*256**2+rgb[1]*256+rgb[2])

# stolen shamelessly fro the python mailing list
def distinct_colors(n):
    colors = []
    step = 1.0/n
    h, s, v = (1, 1, 1)
    for i in range(n):
        r, g, b = map(float2dec, colorsys.hsv_to_rgb(h, s, v))
        colors.append((r, g, b))
        h, s, v = (h-step, s-step, v)
        if h < 0:
            h = 0
        if s < 0:
            s = 0
        if v < 0:
            v = 0
    return map(dec2hex_str, colors)

def datasets(request):
    if not request.user.is_authenticated: # if not logged in in data site, no access
        return render(request, 'mildb/login_error.html')
    return render(request, "mildb/datasets.html", {}) # else return...

def ethnic(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')
    return render(request, "mildb/ethnic.html", {})

def pgag_basic(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    pgags = PGAG.objects.all().order_by("country")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=pgag_basic.csv'

    # header
    line = ['pgagname', 'countryabbrev', 'type']
    writer = csv.writer(response)
    writer.writerow(line)

    # data
    for p in pgags:
        line = (p.name.encode('utf-8'), 
                p.country.abbreviation.encode('utf-8'),
                p.government_relation.encode('utf-8'))
        writer.writerow(line)

    return response


def year_active(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    years = range(1981, 2015)
    data = {}
    for y in years:
        data[str(y)] = 0

    ops = Operation.objects.all()
    for o in ops:
        y = o.year
        data[y] = data[y] + 1    # makes some assumptions...
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=year_active.csv'

    # header
    line = ['year', 'activegroups']
    writer = csv.writer(response)
    writer.writerow(line)

    # data
    for y in years:
        ys = str(y)
        writer.writerow( [y, data[ys]] )

    return response

def country_year_active(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    countries = Country.objects.all().order_by("name")
    
    y2c2o = {}
    years = [str(x) for x in range(1981, 2015)]
    for y in years:
        d = {}
        for c in countries:
            d[c.name] = 0
        y2c2o[y] = d

    ops = Operation.objects.all()
    for o in ops:
        y2c2o[o.year][o.group.country.name] = 1

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=country_year_active.csv'

    # header
    line = ['year']
    writer = csv.writer(response)
    for c in countries:
        line.append(c.abbreviation)
    writer.writerow(line)

    # data
    for y in years:
        line = [y]
        for c in countries:
            action = y2c2o[o.year][c.name]
            line.append(action) 
        writer.writerow(line)

    return response


def sort_groups_by_country(groups):
    country2pgag = {}
    for pgag in groups:
        country2pgag[pgag.country] = []

    for pgag in groups:
        country2pgag[pgag.country].append(pgag)
    
    ck = country2pgag.keys()
    #ck.sort(key=lambda x: x.name)
    results = []
    for el in ck:
        results.append( [el, country2pgag[el]] )
    
    return results


def welcome(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    return render(request, "mildb/welcome.html", {})

def search_country(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(name__icontains=query)
            )
        results = Country.objects.filter(qset).distinct().order_by('name')
    else:
        results = []
    return render(request, "mildb/search_country.html", {
            "results": results,
            "query": query
            })

def member(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    memberchar = MemberCharacteristic.objects.all().order_by("name")
    return render(request, "mildb/member.html", {'mc': memberchar})


def member_detail(request, member_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    member = get_object_or_404(MemberCharacteristic, pk=member_id)    
    groups = PGAG.objects.filter(membership=member)
    results = sort_groups_by_country(groups)
    return render(request, "mildb/member_detail.html", {'member': member, 'results': results})
    

def type(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    return render(request, "mildb/type.html", {'rels': PGAG.GOVREL})


def type_generic(request, type_name):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    for row in PGAG.GOVREL:
        if type_name == row[0]:
            groups = PGAG.objects.filter(government_relation=row[0])
            results = sort_groups_by_country(groups)
            return render(request, "mildb/type_generic.html", {'pname': row[1], 'results': results})
    raise Http404

def target(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    targs = Target.objects.all().order_by("type")
    return render(request, "mildb/target.html", {'targets': targs})


def target_detail(request, target_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    targ = get_object_or_404(Target, pk=target_id)
    groups = PGAG.objects.filter(target=targ)
    results = sort_groups_by_country(groups)

    return render(request, "mildb/target_detail.html", {'results': results, 'target': targ, 'groups': groups})


def search_pgag(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(name__icontains=query)
            )
        results = PGAG.objects.filter(qset).distinct().order_by('name')

        country2pgag = {}
        for pgag in results:
            country2pgag[pgag.country] = []
        for pgag in results:
            country2pgag[pgag.country].append(pgag)

        ck = country2pgag.keys()
        #ck.sort(key=lambda x: x.name)
        results = []
        for el in ck:
            results.append( [el, country2pgag[el]] )

    else:
        results = []
    return render(request, "mildb/search_pgag.html", {
            "results": results,
            "query": query
            })


def year_country_active_pgags(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    countries = Country.objects.all().order_by("name")
    years = range(1981, 2015)
    data = {}
    for c in countries:
        for y in years:
            data[(c, str(y))] = set()

    ops = Operation.objects.all()
    for o in ops:
        c = o.group.country
        y = o.year
        data[(c, y)].add(o.group)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=year-country-active-pgags.csv'

    # header
    line = [None]
    writer = csv.writer(response)
    for c in countries:
        line.append(c.abbreviation)
    writer.writerow(line)

    # data
    for y in years:
        ys = str(y)
        line = [str(y)]
        for c in countries:
            line.append( len(data[c, ys]) ) # size of the set 
        writer.writerow(line)

    return response


def year_country_incidents(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    countries = Country.objects.all().order_by("name")
    years = range(1981, 2015)
    data = {}
    for c in countries:
        for y in years:
            data[(c, str(y))] = 0

    ops = Operation.objects.all()
    for o in ops:
        c = o.group.country
        y = o.year
        data[(c, y)] = data[(c, y)] + int(o.incidents)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=year-country-incidents.csv'

    # header
    line = [None]
    writer = csv.writer(response)
    for c in countries:
        line.append(c.abbreviation)
    writer.writerow(line)

    # data
    for y in years:
        ys = str(y)
        line = [str(y)]
        for c in countries:
            line.append(data[c, ys])
        writer.writerow(line)

    return response

    
def country(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    countries = Country.objects.all().order_by("name")
    groups = PGAG.objects.all()
    ctg = {}
    for c in countries:
        ctg[c] = set()

    for g in groups:
        ctg[g.country].add(g)


    ctglist = []
    for c in countries:
        ctglist.append([c, ctg[c]])

    return render(request, 'mildb/country.html', {'ctglist': ctglist})


def new_country_detail(request, country_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    c = get_object_or_404(Country, pk=country_id)
    groups = PGAG.objects.filter(country=country_id).order_by("name")
    years = range(1981, 2015)
    years2activegroups = {}
    for y in years:
        years2activegroups[str(y)] = set()
    
    for g in groups:
        for y in years:
            ops = Operation.objects.filter(group=g).filter(year=str(y))
            for o in ops:
                if o.incidents > 0:
                    years2activegroups[str(y)].add(g)
    
    data = []
    line = ['']
    for y in years:
        line.append(str(y)[-2:])
    data.append(line)

    for g in groups:
        line = [g]

        dissyear = 10000 # note this magic large number
        if g.date_dissolved is not None:
            dissyear = g.date_dissolved.year

        formyear = 0
        if g.date_formed is not None:
            formyear = g.date_formed.year

        for y in years:
            if g in years2activegroups[str(y)]:
                line.append("1")
            else:
                if (y > dissyear) or (y < formyear):    
                    line.append("-1")
                else:
                    line.append("0")

        data.append(line)

    return render(request, 'mildb/new_country_detail.html', 
        {'country': c, 'groups': groups, 'data': data})


def country_detail(request, country_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    c = get_object_or_404(Country, pk=country_id)
    groups = PGAG.objects.filter(country=country_id).order_by("name")
    years = range(1981, 2015)
    years2incidents = {}
    for y in years:
        years2incidents[y] = 0
    
    for g in groups:
        for y in years:
            year = str(y)
            # figure out how to make fewer calls
            ops = Operation.objects.filter(group=g).filter(year=year)
            for i in ops:
                years2incidents[y] = years2incidents[y] + int(i.incidents)
    
    ys = []
    inc = []
    for y in years:
        ys.append( str(y)[-2:] )
        inc.append( str(years2incidents[y]) )

    gchart = ("http://chart.apis.google.com/chart?" + 
              "chs=600x100&" + 
              "chco=0099CC&" + 
              "chd=t:%s&" % (",".join(inc)) +  
              "chds=0,10&" +
              "chbh=10&" + 
              "cht=bvs&" + 
              "chxt=x,y&" + 
              "chxl=0:%s1:|0|10|" % ("|" + "|".join(ys) + "|") 
              )
    
    return render(request, 'mildb/country_detail.html', 
        {'country': c, 'groups': groups, 'gchart': gchart})

def pgag_detail(request, pgag_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    pgag = get_object_or_404(PGAG, pk=pgag_id)
    for line in PGAG.GOVREL:
        if pgag.government_relation == line[0]:
            return render(request, 'mildb/pgag_detail.html', 
                                      {'pgag': pgag, 'pname': line[1]})


def pgag_evidence(request, pgag_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    pgag = get_object_or_404(PGAG, pk=pgag_id)
    evidence = Evidence.objects.filter(group=pgag_id).order_by('date')
    return render(request, 'mildb/pgag_evidence.html', 
                              {'evidence': evidence, 'pgag': pgag}) 

def link(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    govlink = GovernmentLink.objects.all().order_by("name")
    return render(request, "mildb/link.html", {'lin': govlink})

def link_detail(request, link_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    link = get_object_or_404(GovernmentLink, pk=link_id)    
    groups = PGAG.objects.filter(government_link=link)
    results = sort_groups_by_country(groups)

    return render(request, "mildb/link_detail.html", {'links': link, 'results': results})


def support(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    sup = Support.objects.all().order_by("type")
    return render(request, "mildb/support.html", {'supports': sup})

def support_detail(request, support_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    sup = get_object_or_404(Support, pk=support_id)
    groups = PGAG.objects.filter(support_types=sup)
    results = sort_groups_by_country(groups)

    return render(request, "mildb/support_detail.html", {'results': results, 'support': sup, 'groups': groups})

def termtype(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    termt = TermType.objects.all().order_by("type")
    return render(request, "mildb/termtype.html", {'termtypes': termt})

def termtype_detail(request, termtype_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    termt = get_object_or_404(TermType, pk=termtype_id)
    groups = PGAG.objects.filter(termination_types=termt)
    results = sort_groups_by_country(groups)

    return render(request, "mildb/termtype_detail.html", {'results': results, 'termtype': termt, 'groups': groups})

## Ethnic Characteristics
def ethnictarg(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    ethnict = Ethnic.objects.all().order_by("type")
    return render(request, "mildb/ethnictarg.html", {'ethnic_targs': ethnict})

def ethnictarg_detail(request, ethnictarg_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    ethnict = get_object_or_404(Ethnic, pk=ethnictarg_id)
    groups = PGAG.objects.filter(ethnic_targ=ethnict)
    results = sort_groups_by_country(groups)

    return render(request, "mildb/ethnictarg_detail.html", {'results': results, 'ethnictarg': ethnict, 'groups': groups})

def ethnicmem(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    ethnicm = Ethnic.objects.all().order_by("type")
    return render(request, "mildb/ethnicmem.html", {'ethnic_mems': ethnicm})

def ethnicmem_detail(request, ethnicmem_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    ethnicm = get_object_or_404(Ethnic, pk=ethnicmem_id)
    groups = PGAG.objects.filter(ethnic_mem=ethnicm)
    results = sort_groups_by_country(groups)

    return render(request, "mildb/ethnicmem_detail.html", {'results': results, 'ethnicmem': ethnicm, 'groups': groups})

def ethnicpurp(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    ethnicp = Ethnic.objects.all().order_by("type")
    return render(request, "mildb/ethnicpurp.html", {'ethnic_purps': ethnicp})

def ethnicpurp_detail(request, ethnicpurp_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    ethnicp = get_object_or_404(Ethnic, pk=ethnicpurp_id)
    groups = PGAG.objects.filter(ethnic_purp=ethnicp)
    results = sort_groups_by_country(groups)

    return render(request, "mildb/ethnicpurp_detail.html", {'results': results, 'ethnicpurp': ethnicp, 'groups': groups})


def purpose(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    purp = Purpose.objects.all().order_by("name")
    return render(request, "mildb/purpose.html", {'purpose': purp})


def purpose_detail(request, purpose_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    purpchar = get_object_or_404(Purpose, pk=purpose_id)    
    groups = PGAG.objects.filter(purpose=purpchar)
    results = sort_groups_by_country(groups)
    return render(request, "mildb/purpose_detail.html", {'purpose': purpchar, 'results': results})

## government creating institution


def government_creator(request):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    creator = GovernmentCreator.objects.all().order_by("name")
    return render(request, "mildb/creator.html", {'cre':creator})

def creator_detail(request, link_id):
    if not request.user.is_authenticated:
        return render(request, 'mildb/login_error.html')

    creator = get_object_or_404(GovernmentCreator, pk=creator_id)    
    groups = PGAG.objects.filter(government_creator=creator)
    results = sort_groups_by_country(groups)
    return render(request, "mildb/creator_detail.html", {'creators': govcreate, 'results': results})
