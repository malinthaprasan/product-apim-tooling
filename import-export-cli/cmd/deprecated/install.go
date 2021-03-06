/*
*  Copyright (c) WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
*
*  WSO2 Inc. licenses this file to you under the Apache License,
*  Version 2.0 (the "License"); you may not use this file except
*  in compliance with the License.
*  You may obtain a copy of the License at
*
*    http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing,
* software distributed under the License is distributed on an
* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied.  See the License for the
* specific language governing permissions and limitations
* under the License.
 */

package deprecated

import (
	"github.com/spf13/cobra"
	"github.com/wso2/product-apim-tooling/import-export-cli/cmd"
	"github.com/wso2/product-apim-tooling/import-export-cli/cmd/k8s"
	"github.com/wso2/product-apim-tooling/import-export-cli/utils"
)

const installCmdLiteral = "install"
const installCmdShortDesc = "Install an operator in the configured K8s cluster"
const installCmdLongDesc = "Install an operator in the configured K8s cluster"
const installCmdExamples = utils.ProjectName + ` ` + installCmdLiteral + ` ` + installApiOperatorCmdLiteral

// installCmdDeprecated represents the install command
var installCmdDeprecated = &cobra.Command{
	Use:        installCmdLiteral,
	Short:      installCmdShortDesc,
	Long:       installCmdLongDesc,
	Example:    installCmdExamples,
	Deprecated: "instead use \"" + k8s.K8sCmdLiteral + " " + k8s.K8sInstallCmdLiteral + "\".",
}

func init() {
	cmd.RootCmd.AddCommand(installCmdDeprecated)
}
