

const token = ""
const { Client, Events, GatewayIntentBits, Collection } = require("discord.js")
const { SlashCommandBuilder} = require("discord.js")
const {REST,Routes} = require("discord.js")

// slash commands
const command = {
    data: new SlashCommandBuilder()
        .setName("hey")
        .setDescription("testtesttest"),
    async execute(interaction) {
            await interaction.reply("heloo discord.js")
        }
}

const commands = [
    command.data.toJSON()
];

// discord client main
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

(async () => {
    try {

        await client.login(token)

        console.log('Started refreshing application (/) commands.');
        const rest = new REST({ version: '10' }).setToken(token);
        await rest.put(
            Routes.applicationCommands(client.user.id), // クライアントIDを指定してください
            { body: commands },
        );
        console.log('Successfully reloaded application (/) commands.');
    } catch (error) {
        console.error(error);
    }
})();



//command の登録
client.commands = new Collection()
client.commands.set(command.data.name,command)

client.once(Events.ClientReady, c => {
    console.log(`redey.. ${c.user.tag} login`)
    console.log(c.user.id)
})

client.on(Events.InteractionCreate, async interaction => {
    if (!interaction.isChatInputCommand()) return

    const cmd = interaction.client.commands.get(interaction.commandName)

    if (!cmd) {
        console.error(`${interaction.commandName}は存在しません`)
        return
    }

    try {
        await cmd.execute(interaction)

    } catch (error) {
        console.error(error)
        await interaction.reply({ content: 'エラーが発生しました。', ephemeral: true });
    }

})

client.login(token)

