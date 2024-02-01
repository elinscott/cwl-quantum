# The prospects for using CWL for materials science workflows

## Advantages of using CWL
- workflows are workflow-engine agnostic
- simple workflows are -- in principle -- easy to chain together

## Obstacles to using CWL
- no simple way of writing a python function natively (uses java under the hood)
- workflow engines need to support CWL
- ``records`` do not support defaults, so input files will be very verbose. This might be able to be tweaked (possibly this is CWL-implementation-dependent?)
- writing even slightly complicated workflows becomes tricky. See for example pw.cwl. These difficulties stem from the fact the ``records`` are immutable. This makes manipulation difficult e.g. if I want to update ``ecutwfc`` I have to regenerate an entirely new ``pw_parameters`` object

We could of course invent some new syntax etc but that would be straying from using CWL which is the whole point in the first place.