import * as vscode from 'vscode';

/**
 * HeyGen MCP Server VS Code Extension
 *
 * This extension registers the HeyGen MCP server as an MCP server definition provider,
 * allowing VS Code's language model features to access HeyGen's API for video generation,
 * template management, avatar selection, and more.
 */

export function activate(context: vscode.ExtensionContext) {
	const didChangeEmitter = new vscode.EventEmitter<void>();

	// Register the MCP server definition provider
	const provider: vscode.McpServerDefinitionProvider = {
		onDidChangeMcpServerDefinitions: didChangeEmitter.event,

		provideMcpServerDefinitions: async (_token: vscode.CancellationToken) => {
			const config = vscode.workspace.getConfiguration('heygen-mcp');
			const apiKey = config.get<string>('apiKey');

			const servers: vscode.McpServerDefinition[] = [];

			try {
				// Create stdio server definition for heygen-mcp
				// Always provide the server - resolveMcpServerDefinition will prompt for API key if needed
				// Constructor: McpStdioServerDefinition(label, command, args?, env?, version?)
				const serverDef = new vscode.McpStdioServerDefinition(
					'HeyGen MCP Server',
					'uvx',
					['heygen-mcp-sbroenne'],
					apiKey ? { 'HEYGEN_API_KEY': apiKey } : {},
					'0.1.0'
				);

				servers.push(serverDef);
			} catch (error) {
				const errorMessage = error instanceof Error ? error.message : String(error);
				vscode.window.showErrorMessage(
					`Failed to create HeyGen MCP server definition: ${errorMessage}`
				);
				console.error('HeyGen MCP: Failed to create server definition', error);
			}

			return servers;
		},

		resolveMcpServerDefinition: async (
			server: vscode.McpServerDefinition,
			_token: vscode.CancellationToken
		) => {
			// If this is our HeyGen server and no API key is set, prompt for it
			if (server.label === 'HeyGen MCP Server') {
				const config = vscode.workspace.getConfiguration('heygen-mcp');
				let apiKey = config.get<string>('apiKey');

				if (!apiKey) {
					const promptResult = await vscode.window.showInputBox({
						title: 'HeyGen API Key Required',
						placeHolder: 'Enter your HeyGen API key',
						password: true,
						prompt: 'The HeyGen MCP server requires an API key. Get one from https://www.heygen.com/',
						validateInput: (value: string) => {
							if (!value.trim()) {
								return 'API key cannot be empty';
							}
							return null;
						}
					});

					if (promptResult) {
						apiKey = promptResult;

						// Save to user settings (global) so it works across all workspaces
						await config.update(
							'apiKey',
							apiKey,
							vscode.ConfigurationTarget.Global
						);

						// Notify user
						vscode.window.showInformationMessage(
							'HeyGen API key configured successfully!'
						);

						// Trigger re-evaluation so the server gets the new key
						didChangeEmitter.fire();
					} else {
						// User cancelled
						vscode.window.showWarningMessage(
							'HeyGen MCP server requires an API key to function.'
						);
						return undefined;
					}
				}

				// Return an updated server definition with the API key
				// Constructor: McpStdioServerDefinition(label, command, args?, env?, version?)
				return new vscode.McpStdioServerDefinition(
					'HeyGen MCP Server',
					'uvx',
					['heygen-mcp-sbroenne'],
					{ 'HEYGEN_API_KEY': apiKey },
					'0.1.0'
				);
			}

			return server;
		}
	};

	// Register the provider
	const disposable = vscode.lm.registerMcpServerDefinitionProvider(
		'heygen-mcp.provider',
		provider
	);

	context.subscriptions.push(disposable);

	// Register command to open settings
	const configureCommand = vscode.commands.registerCommand(
		'heygen-mcp.configure',
		async () => {
			const config = vscode.workspace.getConfiguration('heygen-mcp');
			const apiKey = config.get<string>('apiKey');

			if (apiKey) {
				const update = await vscode.window.showInformationMessage(
					'HeyGen API key is already configured. Update it?',
					'Update',
					'Cancel'
				);

				if (update === 'Update') {
					const newKey = await vscode.window.showInputBox({
						title: 'Update HeyGen API Key',
						placeHolder: 'Enter your new HeyGen API key',
						password: true,
						prompt: 'Leave empty to keep current key',
						validateInput: (value: string) => {
							if (value && !value.trim()) {
								return 'API key cannot be only whitespace';
							}
							return null;
						}
					});

					if (newKey !== undefined && newKey !== '') {
						await config.update(
							'apiKey',
							newKey,
							vscode.ConfigurationTarget.Global
						);
						vscode.window.showInformationMessage('API key updated!');
						didChangeEmitter.fire();
					}
				}
			} else {
				const apiKey = await vscode.window.showInputBox({
					title: 'Configure HeyGen API Key',
					placeHolder: 'Enter your HeyGen API key',
					password: true,
					prompt: 'Get your API key from https://www.heygen.com/',
					validateInput: (value: string) => {
						if (!value.trim()) {
							return 'API key cannot be empty';
						}
						return null;
					}
				});

				if (apiKey) {
					await config.update(
						'apiKey',
						apiKey,
						vscode.ConfigurationTarget.Global
					);
					vscode.window.showInformationMessage(
						'HeyGen API key configured successfully! The MCP server will now be available.'
					);
					didChangeEmitter.fire();
				}
			}
		}
	);

	context.subscriptions.push(configureCommand);

	// Register help command
	const helpCommand = vscode.commands.registerCommand(
		'heygen-mcp.help',
		() => {
			vscode.window.showInformationMessage(
				'HeyGen MCP Server provides tools to:\n' +
				'• Generate AI avatar videos\n' +
				'• Manage templates and variables\n' +
				'• Create Avatar IV videos from photos\n' +
				'• Manage avatars, voices, and assets\n' +
				'• Organize with folders\n\n' +
				'Configure your API key first using "HeyGen: Configure API Key"',
				'Configure',
				'Learn More'
			).then(selection => {
				if (selection === 'Configure') {
					vscode.commands.executeCommand('heygen-mcp.configure');
				} else if (selection === 'Learn More') {
					vscode.env.openExternal(
						vscode.Uri.parse('https://github.com/sbroenne/heygen-mcp')
					);
				}
			});
		}
	);

	context.subscriptions.push(helpCommand);

	// Log activation
	console.log('HeyGen MCP VS Code extension activated');
}

export function deactivate() {
	console.log('HeyGen MCP VS Code extension deactivated');
}
