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

package cmd

import (
	"errors"
	"fmt"
	"github.com/spf13/cobra"
	"github.com/wso2/product-apim-tooling/import-export-cli/utils"
	"strings"
)

var flagHttpRequestTimeout int
var flagExportDirectory string
var flagKubernetesMode string
var flagTokenType string

// Set command related Info
const setCmdLiteral = "set"
const setCmdShortDesc = "Set configuration parameters"

const setCmdLongDesc = `Set configuration parameters. Use at least one of the following flags
* --http-request-timeout <time-in-milli-seconds>
* --export-directory <path-to-directory-where-apis-should-be-saved>
* --mode <mode-of-apictl>`

const setCmdExamples = utils.ProjectName + ` ` + setCmdLiteral + ` --http-request-timeout 3600 --export-directory /home/user/exported-apis
` + utils.ProjectName + ` ` + setCmdLiteral + ` --http-request-timeout 5000 --export-directory C:\Documents\exported
` + utils.ProjectName + ` ` + setCmdLiteral + ` --http-request-timeout 5000
` + utils.ProjectName + ` ` + setCmdLiteral + ` --token-type JWT
` + utils.ProjectName + ` ` + setCmdLiteral + ` --token-type OAUTH
` + utils.ProjectName + ` ` + setCmdLiteral + ` --mode kubernetes
` + utils.ProjectName + ` ` + setCmdLiteral + ` --mode default`

// SetCmd represents the 'set' command
var SetCmd = &cobra.Command{
	Use:     "set",
	Short:   setCmdShortDesc,
	Long:    setCmdLongDesc,
	Example: setCmdExamples,
	Run: func(cmd *cobra.Command, args []string) {
		utils.Logln(utils.LogPrefixInfo + setCmdLiteral + " called")
		executeSetCmd(utils.MainConfigFilePath, utils.ExportDirectory)
	},
}

func executeSetCmd(mainConfigFilePath, exportDirectory string) {
	// read the existing config vars
	configVars := utils.GetMainConfigFromFile(mainConfigFilePath)
	//Change Http Request timeout
	if flagHttpRequestTimeout > 0 {
		//Check whether the provided Http time out value is not equal to default value
		if flagHttpRequestTimeout != configVars.Config.HttpRequestTimeout {
			fmt.Println("Http Request Timout is set to : ", flagHttpRequestTimeout)
		}
		configVars.Config.HttpRequestTimeout = flagHttpRequestTimeout
	} else {
		fmt.Println("Invalid input for flag --http-request-timeout")
	}

	//Change Export Directory path
	if flagExportDirectory != "" && utils.IsValid(flagExportDirectory) {
		//Check whether the provided export directory is not equal to default value
		if flagExportDirectory != configVars.Config.ExportDirectory {
			fmt.Println("Export Directory is set to  : ",flagExportDirectory)
		}
		configVars.Config.ExportDirectory = flagExportDirectory
	} else {
		fmt.Println("Invalid input for flag --export-directory")
	}

	//Change Mode
	if flagKubernetesMode != "" {
		if strings.EqualFold(flagKubernetesMode, "kubernetes") || strings.EqualFold(flagKubernetesMode, "k8s") {
			//Check whether the provided mode value is not equal to default value
			if true != configVars.Config.KubernetesMode {
				fmt.Println("Mode is set to : ", flagKubernetesMode)
			}
			configVars.Config.KubernetesMode = true
		} else if strings.EqualFold(flagKubernetesMode, "default") {
			if false != configVars.Config.KubernetesMode {
				fmt.Println("Mode is set to : ", flagKubernetesMode)
			}
			configVars.Config.KubernetesMode = false
		} else {
			utils.HandleErrorAndExit("Error changing mode ",
				errors.New("mode should be set to either kubernetes or none"))
		}
	}

	//Change TokenType
	if flagTokenType != "" {
		if strings.EqualFold(flagTokenType, "jwt") {
			//Check whether the provided token type value is not equal to default value
			if flagTokenType != configVars.Config.TokenType {
				fmt.Println("Token type is set to : ", flagTokenType)
			}
			configVars.Config.TokenType = "JWT"
		} else if strings.EqualFold(flagTokenType, "oauth") {
			if flagTokenType != configVars.Config.TokenType {
				fmt.Println("Token type is set to : ", flagTokenType)
			}
			configVars.Config.TokenType = "OAUTH"
		} else {
			utils.HandleErrorAndExit("Error setting token type ",
				errors.New("Token type should be either JWT or OAuth"))
		}
	}
	utils.WriteConfigFile(configVars, mainConfigFilePath)
}

// init using Cobra
func init() {
	RootCmd.AddCommand(SetCmd)

	var defaultHttpRequestTimeout int
	var defaultExportDirectory string
	var defaultTokenType string

	// read current values in file to be passed into default values for flags below
	mainConfig := utils.GetMainConfigFromFile(utils.MainConfigFilePath)

	if mainConfig.Config.HttpRequestTimeout != 0 {
		defaultHttpRequestTimeout = mainConfig.Config.HttpRequestTimeout
	}

	if mainConfig.Config.ExportDirectory != "" {
		defaultExportDirectory = mainConfig.Config.ExportDirectory
	}

	if mainConfig.Config.TokenType != "" {
		defaultTokenType = mainConfig.Config.TokenType
	}

	SetCmd.Flags().IntVar(&flagHttpRequestTimeout, "http-request-timeout", defaultHttpRequestTimeout,
		"Timeout for HTTP Client")
	SetCmd.Flags().StringVar(&flagExportDirectory, "export-directory", defaultExportDirectory,
		"Path to directory where APIs should be saved")
	SetCmd.Flags().StringVarP(&flagTokenType, "token-type", "t", defaultTokenType,
		"Type of the token to be generated")
	SetCmd.Flags().StringVarP(&flagKubernetesMode, "mode", "m", utils.DefaultEnvironmentName, "If mode is set to \"k8s\", apictl " +
		"is capable of executing Kubectl commands. For example \"apictl get pods\" -> \"kubectl get pods\". To go back " +
		"to the default mode, set the mode to \"default\"")
}
