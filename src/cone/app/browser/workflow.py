from cone.tile import (
    tile,
    Tile,
)
from ..model import Properties
from .ajax import AjaxEvent
from .utils import (
    make_query,
    make_url,
)
from repoze.workflow import get_workflow
from repoze.workflow import WorkflowError

import logging
logger = logging.getLogger('cone.app')


@tile('wf_dropdown', 'templates/wf_dropdown.pt',
      permission='change_state', strict=False)
class WfDropdown(Tile):
    """Transition dropdown.

    If ``do_transition`` is found in ``request.params``, perform given
    transition on ``self.model`` immediately before dropdown gets rendered.
    """

    def do_transition(self):
        """if ``do_transition`` is found on request.params, perform
        transition.
        """
        transition = self.request.params.get('do_transition')
        if not transition:
            return
        workflow = self.workflow
        workflow.transition(self.model, self.request, transition)
        self.model()
        url = make_url(self.request, node=self.model)
        continuation = [AjaxEvent(url, 'contextchanged', '#layout')]
        self.request.environ['cone.app.continuation'] = continuation

    @property
    def workflow(self):
        return get_workflow(self.model.__class__, self.model.workflow_name)

    @property
    def transitions(self):
        self.do_transition()
        ret = list()
        try:
            workflow = self.workflow
            transitions = workflow.get_transitions(
                self.model, self.request, from_state=self.model.state)
        except (WorkflowError, AttributeError), e:
            logger.error("transitions error: %s" % str(e))
            return ret
        workflow_tsf = self.model.workflow_tsf
        for transition in transitions:
            query = make_query(do_transition=transition['name'])
            target = make_url(self.request, node=self.model, query=query)
            props = Properties()
            props.target = target
            props.title = workflow_tsf is not None \
                and workflow_tsf(transition['name']) or transition['name']
            ret.append(props)
        return ret
