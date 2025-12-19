from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.core.config import settings


# ✅ Duas linhas em branco acima para corrigir o erro E302 do Flake8
router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def custom_docs():
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{settings.APP_NAME} | API Docs</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            .glass {{
                background: rgba(30, 41, 59, 0.7);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
        </style>
    </head>
    <body class="bg-[#020617] text-slate-300 font-sans selection:bg-indigo-500/30">
        <div class="max-w-6xl mx-auto py-8 md:py-16 px-4 sm:px-6">

            <header class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 mb-12 border-b border-slate-800 pb-10">
                <div class="space-y-2">
                    <div class="flex items-center gap-3">
                        <span class="bg-indigo-600 text-white text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider">Production</span>
                        <h1 class="text-3xl md:text-5xl font-black text-white tracking-tighter uppercase italic">
                            {settings.APP_NAME} <span class="text-indigo-500 not-italic">v{settings.APP_VERSION}</span>
                        </h1>
                    </div>
                    <p class="text-slate-400 text-sm md:text-base max-w-2xl italic">
                        Documentação técnica consolidada para integração com o ecossistema Kanban.
                    </p>
                </div>
                <div class="flex flex-wrap gap-3 w-full lg:w-auto">
                    <a href="/api/docs" class="flex-1 lg:flex-none text-center bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl font-bold transition-all shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2">
                        <i class="fas fa-bolt"></i> SWAGGER
                    </a>
                    <a href="/api/redoc" class="flex-1 lg:flex-none text-center bg-slate-800 hover:bg-slate-700 text-white px-6 py-3 rounded-xl font-bold transition-all flex items-center justify-center gap-2 border border-slate-700">
                        <i class="fas fa-book"></i> REDOC
                    </a>
                </div>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-8">

                <section class="glass p-6 md:p-8 rounded-3xl space-y-6">
                    <div class="flex items-center gap-3 border-b border-slate-700/50 pb-4">
                        <div class="h-10 w-10 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-400">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <h2 class="text-xl font-bold text-white tracking-tight">Authentication</h2>
                    </div>

                    <div class="space-y-4">
                        <div class="group bg-slate-900/40 p-4 rounded-2xl border border-slate-800 hover:border-blue-500/50 transition-colors">
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-[10px] font-bold text-blue-400 uppercase tracking-widest">Register</span>
                                <span class="px-2 py-1 rounded bg-blue-500/20 text-blue-300 text-[9px] font-bold">POST</span>
                            </div>
                            <code class="text-xs md:text-sm text-slate-200 block truncate">/api/auth/register</code>
                        </div>

                        <div class="group bg-slate-900/40 p-4 rounded-2xl border border-slate-800 hover:border-blue-500/50 transition-colors">
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-[10px] font-bold text-blue-400 uppercase tracking-widest">Login</span>
                                <span class="px-2 py-1 rounded bg-blue-500/20 text-blue-300 text-[9px] font-bold">POST</span>
                            </div>
                            <code class="text-xs md:text-sm text-slate-200 block truncate">/api/auth/login</code>
                        </div>
                    </div>
                </section>

                <section class="glass p-6 md:p-8 rounded-3xl space-y-6">
                    <div class="flex items-center gap-3 border-b border-slate-700/50 pb-4">
                        <div class="h-10 w-10 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-400">
                            <i class="fas fa-layer-group"></i>
                        </div>
                        <h2 class="text-xl font-bold text-white tracking-tight">Tasks Management</h2>
                    </div>

                    <div class="space-y-4">
                        <div class="bg-slate-900/40 p-4 rounded-2xl border border-slate-800">
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-widest">List</span>
                                <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 text-[9px] font-bold">GET</span>
                            </div>
                            <code class="text-xs md:text-sm text-slate-200 block truncate">/api/tasks</code>
                        </div>

                        <div class="bg-slate-900/40 p-4 rounded-2xl border border-slate-800">
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-[10px] font-bold text-purple-400 uppercase tracking-widest">Move</span>
                                <span class="px-2 py-1 rounded bg-purple-500/20 text-purple-300 text-[9px] font-bold">PATCH</span>
                            </div>
                            <code class="text-xs md:text-sm text-slate-200 block truncate">/api/tasks/{{id}}/move</code>
                        </div>
                    </div>
                </section>

            </div>

            <footer class="mt-16 pt-8 border-t border-slate-800 flex flex-col md:flex-row justify-between items-center gap-4 text-slate-500 text-xs text-center md:text-left">
                <p>&copy; 2025 Kanban API System. Todos os direitos reservados.</p>
                <div class="flex gap-6">
                    <span class="flex items-center gap-2"><i class="fas fa-circle text-emerald-500 text-[6px]"></i> API Online</span>
                    <span class="flex items-center gap-2"><i class="fas fa-lock text-indigo-400"></i> JWT Secured</span>
                </div>
            </footer>
        </div>
    </body>
    </html>
    """
