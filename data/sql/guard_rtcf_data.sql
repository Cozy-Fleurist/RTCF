-- ============================================================================
-- Garde-fou anti-écrasement massif sur rtcf_data (id=1)
-- À exécuter UNE FOIS dans Supabase : Dashboard -> SQL Editor -> Run.
--
-- Objectif : bloquer, côté base, toute écriture qui SUPPRIME brutalement
-- beaucoup de joueuses ou beaucoup de coches — quel que soit le code du client
-- (protège même contre un vieil onglet qui exécute encore l'ancien code).
--
-- Seuils (ajustables) :
--   * plus de 3 joueuses existantes supprimées d'un coup       -> REJET
--   * perte de plus de 300 coches (ownership) en une écriture  -> REJET
-- Les opérations normales (cocher/décocher, ajouter/renommer, supprimer 1-2
-- profils) passent sans souci.
-- ============================================================================

create or replace function guard_rtcf_data() returns trigger as $$
declare
  removed_players int;
  old_checks int;
  new_checks int;
begin
  -- joueuses présentes dans l'ANCIEN payload mais absentes du NOUVEAU (par id)
  select count(*) into removed_players
  from jsonb_array_elements(OLD.payload->'players') op
  where not exists (
    select 1 from jsonb_array_elements(NEW.payload->'players') np
    where np->>'id' = op->>'id'
  );

  -- total des coches (somme des longueurs des tableaux "owned")
  select coalesce(sum(jsonb_array_length(f->'owned')),0) into old_checks
  from jsonb_array_elements(OLD.payload->'flowers') f;
  select coalesce(sum(jsonb_array_length(f->'owned')),0) into new_checks
  from jsonb_array_elements(NEW.payload->'flowers') f;

  if removed_players > 3 then
    raise exception 'RTCF garde-fou : % joueuses seraient supprimées d''un coup — écriture bloquée (probable écrasement par une copie périmée).', removed_players;
  end if;

  if new_checks < old_checks - 300 then
    raise exception 'RTCF garde-fou : perte massive de coches (% -> %) — écriture bloquée.', old_checks, new_checks;
  end if;

  return NEW;
end;
$$ language plpgsql;

drop trigger if exists trg_guard_rtcf_data on rtcf_data;
create trigger trg_guard_rtcf_data
  before update on rtcf_data
  for each row execute function guard_rtcf_data();

-- ----------------------------------------------------------------------------
-- Si un jour tu dois faire une opération légitime qui dépasse les seuils
-- (grand nettoyage, restauration…), désactive temporairement le garde-fou :
--     alter table rtcf_data disable trigger trg_guard_rtcf_data;
--     -- ... ton opération ...
--     alter table rtcf_data enable  trigger trg_guard_rtcf_data;
-- ----------------------------------------------------------------------------
