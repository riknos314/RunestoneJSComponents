# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
__author__ = 'isaiahmayerchak'

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

#add directives/javascript/css


class TimedNode(nodes.General, nodes.Element):
    def __init__(self,content):
        super(TimedNode,self).__init__()
        self.timed_options = content


def visit_timed_node(self, node):
#Set options and format templates accordingly

    if 'timelimit' not in node.timed_options:
        node.timed_options['timelimit'] = '60'

    res = TEMPLATE_START % node.timed_options
    self.body.append(res)

def depart_timed_node(self,node):
#Set options and format templates accordingly
    res = TEMPLATE_END % node.timed_options

    self.body.append(res)

#Templates to be formatted by node options
TEMPLATE_START = '''
    <ul data-component="timedAssessment" data-time=%(timelimit)s id="%(divid)s">
    '''

TEMPLATE_END = '''</ul>
    '''
class TimedDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {"timelimit":directives.positive_int}

    def run(self):
        """
            process the timed directive and generate html for output.
            :param self:
            :return:
            .. timed:: identifier
                :timelimit: Number of seconds student has to take the timed assessment
            ...
            """
        self.assert_has_content() # make sure timed has something in it

        self.options['divid'] = self.arguments[0]

        timed_node = TimedNode(self.options)

        self.state.nested_parse(self.content, self.content_offset, timed_node)

        return [timed_node]
