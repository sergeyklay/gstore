;; Copyright (C) 2020-2024 Serghei Iakovlev <gnu@serghei.pl>
;;
;; This file is free software; you can redistribute it and/or
;; modify it under the terms of the GNU General Public License
;; as published by the Free Software Foundation; either version 3
;; of the License, or (at your option) any later version.
;;
;; This file is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.
;;
;; You should have received a copy of the GNU General Public License
;; along with this file.  If not, see <https://www.gnu.org/licenses/>.

;; Eval Buffer with `M-x eval-buffer' to register the newly created template.

(dap-register-debug-template
 "gstore :: Debug Console App"
  (list :type "python"
        :request "launch"
        :name "gstore :: Debug Console App"
        :program "${workspaceFolder}/gstore/__main__.py"
        :cwd "${workspaceFolder}"
        :args '("-o" "myorg" "${workspaceFolder}/output")
        :env '(("GITHUB_TOKEN" . "secret"))))
