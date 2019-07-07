#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re
import paramiko
import yaml

from common import Common


class Demo:
    def __init__(self):
        self.common    = Common()
        self.filename  = 'input.yml'
        #self.category = 'localhost'
        self.category  = 'sakura'
        self.command   = 'ls'
        self.cmd_option_key = self.command
        self.conts     = 0
        self.max_conts = 3


    def get_input(self):
        input = {}
        for key, value in yaml.safe_load(open(self.filename))[self.category].iteritems():
            input[key] = value
        
        return input
    
    def create_commmand(self, cmd_option=None):
        if cmd_option is None:
            return ""
        else:
            return " {opt}".format(opt = ' '.join(cmd_option))
    
    
    def get_output(self, stdout):
        output = {}
        for key in [
            'timestamp', 'bool', 'execute_conts', 'cmd', 'response'
            ]:
            output[key] = ""

        response = []
        #
        #                      #1   #2
        ptn = re.compile(r'\s*(\S+)(\n*)\s*')
        #How to enumerate a range of numbers starting at 1
        #https://stackoverflow.com/questions/3303608/how-to-enumerate-a-range-of-numbers-starting-at-1
        #enumerate(sequence, start=1)
        try:
            for line in stdout:
                if ptn.search(str(line)):
                    response.append(ptn.search(str(line)).group(1))
                else:
                    response.append(str(line))
                
        except:
            pass
        
        if len(response) == 0:
            output.update({
                'bool'    : False,
                'response': None
            })
        else:
            output.update({
                'bool'    : True,
                'response': ', '.join(response)
            })
        
        output.update({
            'cmd': self.command,
            'timestamp' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        return output
    

    def main(self):
        outputs = []
        input = self.get_input()
        self.command = self.command + self.create_commmand(input['cmd_option'][self.cmd_option_key])
        while True:
            try:
                stdin, stdout, stderr = self.common.execute_command(input, self.command)
                current_output = self.get_output(stdout)
                self.conts += 1
                if current_output['bool']:
                    current_output.update({'execute_conts': self.conts})
                    break
                else:
                    if self.conts < self.max_conts:
                        current_output = None
                        continue
                    else:
                        current_output.update({'execute_conts': self.conts})
                        break
            except:
                current_output = None
                break

        if current_output is None:
            outputs = None
        else:
            outputs.append(current_output)

        return outputs