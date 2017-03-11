set nocompatible           " use vim defaults (much better!)
set encoding=utf-8
set nobackup               " disable backup and swap files because they cause more problems than they solve
set noswapfile             " disable backup and swap files because they cause more problems than they solve
set ruler                  " show the cursor position all the time
set history=50             " keep 50 lines of command line history
set laststatus=2           " enable airline to display status bar
set autoindent             " always indent
set bs=indent,eol,start    " allow backspacing over everything in insert mode
set splitbelow             " make the new window appear below the current window
set splitright             " make the new window appear to the right of the current window
set clipboard=unnamed      " system clipboard for osx
set shiftwidth=4           " Use 4 spaces for tabs
set tabstop=4              " Use 4 spaces for tabs
set expandtab
set smartindent

let python_highlight_all=1 " make python pretty
syntax on                  " syntax highlighting on
filetype plugin on
filetype plugin indent on  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
" call vundle#begin('~/.vim/vundle_plugins')
" let Vundle manage Vundle, required
Plugin 'altercation/vim-colors-solarized'
Plugin 'gmarik/vundle.vim'
Plugin 'godlygeek/tabular'
" Plugin 'jnurmine/zenburn'
" Plugin 'jtratner/vim-flavored-markdown'
" Plugin 'junegunn/goyo.vim'
" Plugin 'lokaltog/powerline', {'rtp': 'powerline/bindings/vim/'}
" Plugin 'nvie/vim-flake8'
" Plugin 'reedes/vim-pencil'
" Plugin 'scrooloose/nerdtree'
" Plugin 'scrooloose/syntastic'
Plugin 'tpope/vim-commentary'
" Plugin 'tpope/vim-markdown'
" Plugin 'gabrielelana/vim-markdown'
" Plugin 'valloric/youcompleteme'
" Plugin 'vim-scripts/indentpython.vim'
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
" Add all your plugins here (note older versions of Vundle used Bundle instead of Plugin)
" All of your Plugins must be added before the following line
call vundle#end()            " required

" source vim configuration upon save
if has ('autocmd') " remain compatible with earlier versions
	augroup vimrc     " source vim configuration upon save
		autocmd! bufwritepost $myvimrc source % | echom "reloaded " . $myvimrc | redraw
		autocmd! bufwritepost $mygvimrc if has('gui_running') | so % | echom "reloaded " . $mygvimrc | endif | redraw
	augroup end
endif " has autocmd

" split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <c-k> <c-w><c-k>
nnoremap <c-l> <c-w><c-l>
nnoremap <c-h> <c-w><c-h>

" proper pep8 indentation
au bufnewfile,bufread *.py
			\ set tabstop=4 |
			\ set softtabstop=4 |
			\ set shiftwidth=4 |
			\ set textwidth=79 |
			\ set expandtab |
			\ set autoindent |
			\ set fileformat=unix

" mark extra whitespace as bad, and probably color it red
highlight badwhitespace ctermbg=red guibg=red
au bufread,bufnewfile *.py,*.pyw,*.c,*.h match badwhitespace /\s\+$/

" " " youcompleteme
" " " former line ensures that the autocomplete window goes away when you’re done
" " " with it, and the latter defines a shortcut for goto definition
" " let g:ycm_autoclose_preview_window_after_completion=1
" " map <leader>g  :ycmcompleter gotodefinitionelsedeclaration<cr>


" " tabularize mapping
let mapleader=' '
" if exists(":Tabularize")
nmap <Leader>t= :Tabularize /=<CR>
vmap <Leader>t= :Tabularize /=<CR>
nmap <Leader>t: :Tabularize /:<CR>
vmap <Leader>t: :Tabularize /:<CR>
nmap <Leader>t" :Tabularize /"<CR>
vmap <Leader>t" :Tabularize /"<CR>
" endif

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

set background=dark        " set background color
colorscheme solarized      " color scheme
