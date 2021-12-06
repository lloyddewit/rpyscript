"""
RPyScript <one line to give the program's name and a brief idea of what it does.>TODO
Copyright (C) 2021-2022 IDEMS International, Stephen Lloyd

This file is part of RPyScript.

    RPyScript is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RPyScript is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with RPyScript.  If not, see <https://www.gnu.org/licenses/>.
"""
class RScript:
    def __init__(self, script_str) -> None:
        self.script_str = script_str

    def get_lst_lexemes(self, script_str):
        return ['a', '::', 'b']

