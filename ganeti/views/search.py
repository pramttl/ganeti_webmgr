import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from haystack.query import SearchQuerySet
from ganeti.models import VirtualMachine, Cluster, Node


@login_required
def suggestions(request):
    ''' Return a list of search results for the autocomplete search box.

    Return a list of search results for the query in the GET parameter `term` 
    as a JSON object. If `term` does not exist, just return a blank list.

    The format consists of a list of objects representing the object name and 
    the object type. Here's an example:

        [
            {
                'value':    'foo',
                'type':     'vm',
            },
            {
                'value':    'bar',
                'type':     'vm',
            },
            {
                'value':    'herp',
                'type':     'cluster',
            },
            {
                'value':    'derp',
                'type':     'node',
            }
        ]
    '''
    # Get the query from the GET param
    query = request.GET.get('term', None)

    # Start out with an empty result objects list
    result_objects = []

    # If a query actually does exist, construct the result objects
    if query is not None:

        # Perform the actual query on the Haystack search query set
        results = SearchQuerySet().autocomplete(content_auto=query)

        # Construct the result objects
        for result in results:
            result_object = {}
            result_object['value'] = result.content_auto
            if result.model_name == 'virtualmachine':
                result_object['type'] = 'vm'
            elif result.model_name == 'cluster':
                result_object['type'] = 'cluster'
            elif result.model_name == 'node':
                result_object['type'] = 'node'
            else:
                result_object['type'] = 'unknown'
            result_objects.append(result_object)

    # Return the results list as a json object
    return HttpResponse(json.dumps(result_objects, indent=4), 
            mimetype='application/json')

@login_required
def detail_lookup(request):
    object_type = request.GET.get('type', None)
    hostname = request.GET.get('hostname', None)
    URL = []
    if object_type and hostname:
        try:
            if object_type == 'vm':
                vm = VirtualMachine.objects.filter(hostname=hostname)[0]
                URL.append(reverse('instance-detail', 
                        args=[
                            vm.cluster.slug, 
                            vm.hostname
                        ]))
            elif object_type == 'cluster':
                cluster = Cluster.objects.filter(hostname=hostname)[0]
                URL.append(reverse('cluster-detail', args=[cluster.slug]))
            elif object_type == 'node':
                node = Node.objects.filter(hostname=hostname)[0]
                URL.append(reverse('node-detail', 
                        args=[
                            node.cluster.slug, 
                            node.hostname
                        ]))

        # If an object can't be found, just return a blank URL
        except IndexError:
            pass 

    return HttpResponse(json.dumps(URL, indent=4), mimetype='application/json')
