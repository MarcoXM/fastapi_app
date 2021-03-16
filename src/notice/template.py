import os 


### setting up the diretory 

## get the file path
FILE_PATH = os.path.abspath(__file__)
BASE_PATH = os.path.dirname(FILE_PATH)
TEMPLATE_FOLDER_PATH = os.path.join(BASE_PATH,"email_template")


class Template:
    def __init__(self, template_name = "", context = None, *args , **kwargs):
        self.template_name = template_name
        self.context = context 


    def _get_template(self):

        template_file_path = os.path.join(TEMPLATE_FOLDER_PATH, self.template_name)
        if not os.path.exists(template_file_path):
            raise Exception(f"This {self.template_name} is not exists, please check again !")

        template_str = ""
        with open(template_file_path, 'r') as f:
            template_str = f.read()

        return template_str

    def render(self, context = None):
        render_txt = context
        if self.context is not None:
            render_txt = self.context

        if not isinstance(render_txt, dict):
            render_txt = {}

        template_str = self._get_template()
        return template_str.format(**render_txt)




if __name__ =="__main__":
    t = Template("hello.html",{"recipient_name":"Marco"})
    print(t.render())