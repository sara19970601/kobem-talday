-- «Көркем шығарманы талдау»: бұлттағы жұмыс кестесі.
-- Supabase → SQL Editor → New query → осы файлды толық қойып, Run басыңыз. Қайта іске қосуға болады.
-- Әр пайдаланушыға бір жол: «Талдауларым» мен «Зертхана» деректері бір JSON (data) ішінде.

create table if not exists public.user_data (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  data       jsonb not null,
  updated_at timestamptz not null default now(),
  -- Бір пайдаланушының деректері 1 000 000 таңбадан аспасын (сайт та осыны тексереді).
  constraint user_data_size check (length(data::text) < 1000000)
);

-- Жол деңгейіндегі қорғаныс (RLS): әркім тек өз жолын көреді және өзгертеді.
alter table public.user_data enable row level security;

drop policy if exists "user_data: өз жолын оқу"     on public.user_data;
drop policy if exists "user_data: өз жолын қосу"    on public.user_data;
drop policy if exists "user_data: өз жолын өзгерту" on public.user_data;
drop policy if exists "user_data: өз жолын өшіру"   on public.user_data;

create policy "user_data: өз жолын оқу" on public.user_data
  for select to authenticated using (auth.uid() = user_id);
create policy "user_data: өз жолын қосу" on public.user_data
  for insert to authenticated with check (auth.uid() = user_id);
create policy "user_data: өз жолын өзгерту" on public.user_data
  for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "user_data: өз жолын өшіру" on public.user_data
  for delete to authenticated using (auth.uid() = user_id);

-- Кірмеген қонаққа (anon) кестеге жол жоқ; кірген пайдаланушыға — тек жоғарыдағы ережелер бойынша.
revoke all on public.user_data from anon;
grant select, insert, update, delete on public.user_data to authenticated;
