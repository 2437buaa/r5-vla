import ast
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('materialize',ROOT/'scripts/materialize.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)


class MaterializationTests(unittest.TestCase):
    def config(self):
        values=json.loads((ROOT/'config/site.example.json').read_text())
        values.update(MASTER_CAN_SERIAL='TEST_MASTER',FOLLOWER_CAN_SERIAL='TEST_FOLLOWER')
        return values

    def test_complete_render_no_hardware(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'runtime';rows=mod.render(self.config(),out)
            self.assertGreater(len(rows),50)
            for row in rows:
                self.assertFalse(mod.TOKEN.search((out/row['path']).read_text()))
                if row['path'].endswith('.py'):
                    ast.parse((out/row['path']).read_text(),filename=row['path'])
            record=json.loads((out/'MATERIALIZED.json').read_text())
            self.assertFalse(record['hardware_started']);self.assertFalse(record['jobs_submitted'])

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):mod.render(self.config(),Path(tmp))

    def test_missing_key_rejected(self):
        config=self.config();del config['ROS_WORKSPACE']
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):mod.render(config,Path(tmp)/'out')
            self.assertFalse((Path(tmp)/'out').exists())

    def test_unset_identity_rejected(self):
        config=self.config();config['MASTER_CAN_SERIAL']='REPLACE_MASTER_CAN_SERIAL'
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):mod.render(config,Path(tmp)/'out')

    def test_shell_or_python_injection_rejected(self):
        for value in ['/tmp/a;touch /tmp/x',"/tmp/a'b",'/tmp/$(id)','/tmp/with space','/tmp/a\nb']:
            config=self.config();config['ROS_WORKSPACE']=value
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError):mod.render(config,Path(tmp)/'out')


if __name__=='__main__':unittest.main()
