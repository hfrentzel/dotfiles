return {
    cmd = { 'rust-analyzer' },
    filetypes = { 'rust' },
    root_markers = { '.git' },
    settings = {
        ['rust-analyzer'] = {
            check = {
                command = 'clippy',
            },
        },
    },
    init_options = {
        check = {
            command = 'clippy',
        },
    },
}
