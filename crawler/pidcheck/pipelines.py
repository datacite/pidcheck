
class PIDMetadataIDPipeline():
    """Looks at scraped metadata to see what ID's match our known PID identifier"""
    def process_item(self, item, spider):
        item['pid_meta_match'] = []
        item['pid_meta_different'] = []

        # The metadata ID's we know about that we want to match against
        metadata_types = [
            'dc_identifier',
            'citation_doi',
            'schema_org_id'
        ]

        for type in metadata_types:
            if type in item:
                if item[type]:
                    if item['pid'] in item[type]:
                        item['pid_meta_match'].append(type)
                    else:
                        item['pid_meta_different'].append(type)

        return item


class PIDScorePipeline():
    def process_item(self, item, spider):
        pass