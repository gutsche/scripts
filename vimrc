set encoding=utf-8
if v:lang =~ "utf8$" || v:lang =~ "UTF-8$"
    set fileencodings=ucs-bom,utf-8,latin1
endif

set nocompatible        " Use Vim defaults (much better!)
set bs=indent,eol,start " allow backspacing over everything in insert mode
set ai                  " always set autoindenting on
" Disable backup and swap files because they cause more problems than they solve
set nobackup            " Disable backup and swap files because they cause more problems than they solve
set noswapfile          " Disable backup and swap files because they cause more problems than they solve
set viminfo='20,\"50    " read/write a .viminfo file, don't store more than 50 lines of registers
set history=50          " keep 50 lines of command line history
set ruler               " show the cursor position all the time

" filetype off            " required, not sure what it does
filetype plugin on

" Switch syntax highlighting on, when the terminal has colors
" Also switch on highlighting the last used search pattern.
if &t_Co > 2 || has("gui_running")
    syntax on
    set hlsearch
endif
if &term=="xterm"
    set t_Co=8
    set t_Sb=^[[4%dm
    set t_Sf=^[[3%dm
endif

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/.vim/vundle_plugins')
" let Vundle manage Vundle, required
Plugin 'altercation/vim-colors-solarized'
Plugin 'gmarik/vundle.vim'
Plugin 'godlygeek/tabular'
Plugin 'jnurmine/zenburn'
Plugin 'jtratner/vim-flavored-markdown'
Plugin 'junegunn/goyo.vim'
Plugin 'lokaltog/powerline', {'rtp': 'powerline/bindings/vim/'}
Plugin 'nvie/vim-flake8'
Plugin 'scrooloose/nerdtree'
Plugin 'scrooloose/syntastic'
Plugin 'tmhedberg/simpylfold'
Plugin 'tpope/vim-commentary'
Plugin 'valloric/youcompleteme'
Plugin 'vim-scripts/indentpython.vim'
" Add all your plugins here (note older versions of Vundle used Bundle instead of Plugin)
" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

" docstring for folded code with SimplyFold
let g:SimpylFold_docstring_preview=1

" split screen
set splitbelow
set splitright

" split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" Enable folding
set foldmethod=indent
set foldlevel=99

" Enable folding with the spacebar
nnoremap <space> za

" proper PEP8 indentation
au BufNewFile,BufRead *.py
            \ set tabstop=4 |
            \ set softtabstop=4 |
            \ set shiftwidth=4 |
            \ set textwidth=79 |
            \ set expandtab |
            \ set autoindent |
            \ set fileformat=unix

" mark extra whitespace as bad, and probably color it red
highlight BadWhitespace ctermbg=red guibg=red
au BufRead,BufNewFile *.py,*.pyw,*.c,*.h match BadWhitespace /\s\+$/

" YouCompleteMe
" former line ensures that the autocomplete window goes away when you’re done
" with it, and the latter defines a shortcut for goto definition
let g:ycm_autoclose_preview_window_after_completion=1
map <leader>g  :YcmCompleter GoToDefinitionElseDeclaration<CR>

" make python code pretty
let python_highlight_all=1
syntax on

" colorscheme
set background=dark
colorscheme solarized

" line numbering
set nu

" system clipboard for OSX
set clipboard=unnamed

" tabularize mapping
let mapleader=','
if exists(":Tabularize")
    nmap <Leader>a= :Tabularize /=<CR>
    vmap <Leader>a= :Tabularize /=<CR>
    nmap <Leader>a: :Tabularize /:<CR>
    vmap <Leader>a: :Tabularize /:<CR>
endif

" tabularize auto indent table delimited with |
inoremap <silent> <Bar>   <Bar><Esc>:call <SID>align()<CR>a
function! s:align()
    let p = '^\s*|\s.*\s|\s*$'
    if exists(':Tabularize') && getline('.') =~# '^\s*|' && (getline(line('.')-1) =~# p || getline(line('.')+1) =~# p)
        let column = strlen(substitute(getline('.')[0:col('.')],'[^|]','','g'))
        let position = strlen(matchstr(getline('.')[0:col('.')],'.*|\s*\zs.*'))
        Tabularize/|/l1
        normal! 0
        call search(repeat('[^|]*|',column).'\s\{-\}'.repeat('.',position),'ce',line('.'))
    endif
endfunction

" GitHub flavored markdown via vim-flavored-markdown
augroup markdown
    au!
    au BufNewFile,BufRead *.md,*.markdown setlocal filetype=ghmarkdown
augroup END

" Use 4 spaces for tabs
set shiftwidth=4
set tabstop=4
set expandtab
set smartindent

" Quickly edit/reload this configuration file
nnoremap gev :e $MYVIMRC<CR>
nnoremap gsv :so $MYVIMRC<CR>

if has ('autocmd') " Remain compatible with earlier versions
    augroup vimrc     " Source vim configuration upon save
        autocmd! BufWritePost $MYVIMRC source % | echom "Reloaded " . $MYVIMRC | redraw
        autocmd! BufWritePost $MYGVIMRC if has('gui_running') | so % | echom "Reloaded " . $MYGVIMRC | endif | redraw
    augroup END
endif " has autocmd
